"""Unit tests for the Router Agent."""

from unittest.mock import AsyncMock, patch

import pytest
from app.agents.router_agent import RouterAgent


class TestRouterAgent:
    """Tests for the RouterAgent."""

    @pytest.mark.asyncio
    @patch("app.agents.router_agent.ChatOpenAI")
    async def test_route_rag_query(self, mock_llm_cls):
        """Should route queries about documents to RAG."""
        # Mock the structured output chain
        mock_llm_instance = mock_llm_cls.return_value
        mock_chain = AsyncMock()
        mock_chain.ainvoke.return_value.destination = "rag"
        mock_chain.ainvoke.return_value.reasoning = "User asks about a file."

        # The agent does: prompt | llm.with_structured_output(...)
        # We need to mock the pipe chain
        with patch("app.agents.router_agent.router_prompt") as mock_prompt:
            mock_pipe = AsyncMock()
            mock_prompt.__or__.return_value = mock_pipe
            mock_pipe.ainvoke.return_value.destination = "rag"
            mock_pipe.ainvoke.return_value.reasoning = "User asks about a file."

            agent = RouterAgent()
            # We bypass the complex chain mocking by just mocking the router attribute usually,
            # but here we test the init logic minimally or just mock the router property.
            agent.router = mock_pipe  # Inject mock chain directly

            decision = await agent.route("Summarize the uploaded PDF.")

            assert decision.destination == "rag"
            assert decision.reasoning == "User asks about a file."

    @pytest.mark.asyncio
    @patch("app.agents.router_agent.ChatOpenAI")
    async def test_route_sql_query(self, mock_llm_cls):
        """Should route analytics queries to SQL."""
        mock_pipe = AsyncMock()
        mock_pipe.ainvoke.return_value.destination = "sql"
        mock_pipe.ainvoke.return_value.reasoning = "Query about customers."

        agent = RouterAgent()
        agent.router = mock_pipe

        decision = await agent.route("How many customers in London?")

        assert decision.destination == "sql"

    @pytest.mark.asyncio
    @patch("app.agents.router_agent.ChatOpenAI")
    async def test_route_general_chat(self, mock_llm_cls):
        """Should route generic queries to general_chat."""
        mock_pipe = AsyncMock()
        mock_pipe.ainvoke.return_value.destination = "general_chat"
        mock_pipe.ainvoke.return_value.reasoning = "Greeting."

        agent = RouterAgent()
        agent.router = mock_pipe

        decision = await agent.route("Hello there!")

        assert decision.destination == "general_chat"

    @pytest.mark.asyncio
    @patch("app.agents.router_agent.ChatOpenAI")
    async def test_router_fallback_on_error(self, mock_llm_cls):
        """Should fallback to general_chat on exception."""
        mock_pipe = AsyncMock()
        mock_pipe.ainvoke.side_effect = Exception("OpenAI Error")

        agent = RouterAgent()
        agent.router = mock_pipe

        decision = await agent.route("Tricky query")

        assert decision.destination == "general_chat"
        assert "Router error" in decision.reasoning
