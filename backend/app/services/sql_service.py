"""SQL Service for Text-to-SQL pipeline."""

import logging

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.prompts.text_to_sql import text_to_sql_prompt
from app.agents.tools.sql_db import NorthwindDatabase
from app.api.v1.schemas.chat import MessageResponse
from app.config import settings
from app.services import history_service

logger = logging.getLogger(__name__)

# Initialize DB tool (singleton-ish)
# Ideally this should be a dependency, but for simplicity we instantiate here
_northwind_db = None


def get_northwind_db() -> NorthwindDatabase:
    """Get or create the Northwind database wrapper."""
    global _northwind_db
    if _northwind_db is None:
        _northwind_db = NorthwindDatabase()
    return _northwind_db


async def process_sql_question(
    session_id: str | None,
    user_message: str,
    db: AsyncSession,
) -> MessageResponse:
    """Process a natural language question using the Text-to-SQL pipeline.

    Flow:
    1. Save user message.
    2. Get SQL schema.
    3. Generate SQL using LLM.
    4. Validate and Execute SQL.
    5. Synthesize answer (optional, or return raw result for now).
       (For Phase 4, we'll return the result description as the answer).
    6. Save assistant answer.

    Args:
        session_id: Client-provided session ID.
        user_message: User question.
        db: Async database session.

    Returns:
        MessageResponse.
    """
    # 1. Session & User Message
    session = await history_service.get_or_create_session(session_id, db)
    await history_service.add_message(
        session_id=session.id,
        role="user",
        content=user_message,
        db=db,
    )

    # 2. Get DB & Schema
    nw_db = get_northwind_db()
    # For Phase 4, we just dump all table schemas.
    # In a real app, we might check which tables are relevant first.
    tables = nw_db.list_tables()
    schema_str = nw_db.get_schema(tables) if tables else "No tables found."

    # 3. Generate SQL
    llm = ChatOpenAI(
        model=settings.openai_chat_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )
    chain = text_to_sql_prompt | llm | StrOutputParser()

    try:
        generated_sql = await chain.ainvoke({"schema": schema_str, "question": user_message})
        generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        logger.info("Generated SQL: %s", generated_sql)

        # 4. Execute SQL
        result_str = nw_db.run_query(generated_sql)

        # 5. Synthesize Answer
        # We'll just format the result nicely for now.
        # Future: Use LLM to rephrase result naturalistically.
        answer = f"Executed Query: {generated_sql}\n\nResult:\n{result_str}"

        metadata = {
            "query": generated_sql,
            "context_source": "northwind_db",
        }

    except Exception as e:
        logger.exception("Text-to-SQL failed")
        answer = f"I encountered an error trying to query the database: {e}"
        metadata = {"error": str(e)}

    # 6. Save Assistant Message
    saved_msg = await history_service.add_message(
        session_id=session.id,
        role="assistant",
        content=answer,
        db=db,
        metadata=metadata,
        route_decision="text_to_sql",
    )

    return MessageResponse(
        id=str(saved_msg.id),
        role=saved_msg.role,
        content=saved_msg.content,
        route_decision=saved_msg.route_decision,
        metadata=saved_msg.metadata_,
        created_at=saved_msg.created_at,
    )
