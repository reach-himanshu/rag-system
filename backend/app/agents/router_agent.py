"""Router Agent logic using structured output."""

import logging
from typing import Literal

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.agents.prompts.router import router_prompt
from app.config import settings

logger = logging.getLogger(__name__)


class RouteQuery(BaseModel):
    """Routing decision for a user query."""

    destination: Literal["rag", "sql", "general_chat"] = Field(
        ...,
        description="The target pipeline for the query.",
    )
    reasoning: str = Field(
        ...,
        description="Brief explanation for why this destination was chosen.",
    )


class RouterAgent:
    """Agent that routes queries to the appropriate pipeline."""

    def __init__(self):
        llm = ChatOpenAI(
            model=settings.openai_chat_model,
            api_key=settings.openai_api_key,
            temperature=0,
        )
        # Use structured output for reliable routing
        self.router = router_prompt | llm.with_structured_output(RouteQuery)

    async def route(self, query: str) -> RouteQuery:
        """Decide where to route the query.

        Args:
            query: The user's input message.

        Returns:
            RouteQuery object containing destination and reasoning.
        """
        try:
            decision = await self.router.ainvoke({"input": query})
            logger.info(
                "Router decision: %s (Reason: %s)",
                decision.destination,
                decision.reasoning,
            )
            return decision
        except Exception as e:
            logger.error("Router failed: %s", e)
            # Fallback to general chat or RAG on error
            return RouteQuery(
                destination="general_chat",
                reasoning=f"Router error: {e}",
            )


# Singleton-ish instance
_router_agent = None


def get_router_agent() -> RouterAgent:
    """Get or create the RouterAgent instance."""
    global _router_agent
    if _router_agent is None:
        _router_agent = RouterAgent()
    return _router_agent
