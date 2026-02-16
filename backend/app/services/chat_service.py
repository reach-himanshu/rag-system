"""Chat service orchestration with Routing and Streaming."""

import logging
from collections.abc import AsyncGenerator

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.prompts.document_qa import prompt_template as rag_prompt
from app.agents.prompts.text_to_sql import text_to_sql_prompt
from app.agents.router_agent import get_router_agent
from app.agents.tools.document_search import search_documents
from app.config import settings
from app.services import history_service
from app.services.sql_service import get_northwind_db

logger = logging.getLogger(__name__)


async def process_message_stream(
    session_id: str | None,
    user_message: str,
    db: AsyncSession,
    mode: str = "auto",
) -> AsyncGenerator[str, None]:
    """Process a message and yield SSE event data strings.

    Yields JSON strings in SSE format:
    data: {"type": "token", "content": "..."}
    data: {"type": "metadata", "metadata": {...}}
    data: {"type": "done", "content": ""}
    data: {"type": "error", "content": "..."}
    """
    try:
        # 1. Session Management
        session = await history_service.get_or_create_session(session_id, db)

        # Save User Message
        await history_service.add_message(
            session_id=session.id,
            role="user",
            content=user_message,
            db=db,
        )

        # 2. Routing
        route_decision = mode
        if mode == "auto":
            router = get_router_agent()
            decision = await router.route(user_message)
            route_decision = decision.destination
            # Emit routing metadata
            yield f'{{"type": "metadata", "metadata": {{"route": "{route_decision}", "reasoning": "{decision.reasoning}"}}}}'

        # 3. Execution Pipeline (RAG vs SQL vs General)
        if route_decision == "sql":
            # --- SQL PIPELINE ---
            # For SQL, strict streaming is harder because we need the full query first.
            # We'll stream the "thinking" steps optionally, but for now just yield the result chunked.

            nw_db = get_northwind_db()
            tables = nw_db.list_tables()
            schema_str = nw_db.get_schema(tables) if tables else ""

            llm = ChatOpenAI(model=settings.openai_chat_model, api_key=settings.openai_api_key, temperature=0, streaming=True)
            chain = text_to_sql_prompt | llm | StrOutputParser()

            # Generate SQL
            generated_sql = ""
            async for chunk in chain.astream({"schema": schema_str, "question": user_message}):
                # We don't stream the SQL generation to the user typically, unless debugging.
                # Let's collect it.
                generated_sql += chunk

            generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()

            # Execute
            result_str = nw_db.run_query(generated_sql)
            answer = f"Executed Query: {generated_sql}\n\nResult:\n{result_str}"

            # Streaming the "answer" (which is static here, but we treat it as a stream)
            yield f'{{"type": "token", "content": "{answer.replace(chr(10), "\\\\n")}"}}'

            metadata = {"query": generated_sql, "context_source": "northwind_db"}

        elif route_decision == "rag":
            # --- RAG PIPELINE ---
            context_str = await search_documents.ainvoke(user_message)

            # Retrieve History
            history_orm = await history_service.get_session_history(str(session.id), db, limit=10)
            history_lc = [
                HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content)
                for m in history_orm
            ]

            llm = ChatOpenAI(model=settings.openai_chat_model, api_key=settings.openai_api_key, temperature=0, streaming=True)
            chain = rag_prompt | llm | StrOutputParser()

            answer = ""
            async for chunk in chain.astream({"context": context_str, "history": history_lc, "input": user_message}):
                answer += chunk
                # Escape newlines for JSON usage in data: field
                safe_chunk = chunk.replace("\n", "\\n").replace('"', '\\"')
                yield f'{{"type": "token", "content": "{safe_chunk}"}}'

            metadata = {"context_source": "document_search"}

        else:
            # --- GENERAL CHAT PIPELINE ---
            history_orm = await history_service.get_session_history(str(session.id), db, limit=10)
            history_lc = [
                HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content)
                for m in history_orm
            ]
            history_lc.append(HumanMessage(content=user_message))

            llm = ChatOpenAI(model=settings.openai_chat_model, api_key=settings.openai_api_key, temperature=0.7, streaming=True)

            answer = ""
            async for chunk in llm.astream(history_lc):
                content = chunk.content
                answer += content
                safe_chunk = content.replace("\n", "\\n").replace('"', '\\"')
                yield f'{{"type": "token", "content": "{safe_chunk}"}}'

            metadata = {"context_source": "general_chat"}

        # 4. Save Assistant Message
        await history_service.add_message(
            session_id=session.id,
            role="assistant",
            content=answer,
            db=db,
            metadata=metadata,
            route_decision=route_decision,
        )

        # Done event
        yield '{"type": "done", "content": ""}'

    except Exception as e:
        logger.exception("Streaming failed")
        yield f'{{"type": "error", "content": "{str(e)}"}}'
