"""Unit tests for chat service RAG pipeline."""

import json
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.db.models import ChatSession
from app.services import chat_service


@pytest.fixture
def mock_db():
    """Create a mock async database session."""
    return AsyncMock()


@pytest.fixture
def mock_session():
    """Create a mock ChatSession."""
    return ChatSession(id=uuid.uuid4())


@pytest.mark.asyncio
async def test_successful_rag_flow(mock_db, mock_session):
    """Should execute full RAG flow: history -> search -> llm -> save."""
    # Setup Mock Chain to yield chunks
    mock_chain = AsyncMock()

    async def async_gen(*args, **kwargs):
        yield "chunk1"
        yield "chunk2"

    mock_chain.astream = async_gen

    with (
        patch("app.services.chat_service.rag_prompt") as mock_rag_prompt,
        patch("app.services.chat_service.history_service") as mock_history,
        patch("app.services.chat_service.search_documents") as mock_search,
        patch("app.services.chat_service.get_router_agent") as mock_get_router,
    ):
        # 1. Setup History
        mock_history.get_or_create_session = AsyncMock(return_value=mock_session)
        mock_history.get_session_history = AsyncMock(return_value=[])
        mock_history.add_message = AsyncMock()

        # 2. Setup Router
        mock_router_agent = AsyncMock()
        mock_router_agent.route.return_value.destination = "rag"
        mock_router_agent.route.return_value.reasoning = "test reasoning"
        mock_get_router.return_value = mock_router_agent

        # 3. Setup Search
        mock_search.ainvoke = AsyncMock(return_value="[Document 1] Context")

        # 4. Setup LLM Chain Pipe
        # prompt | llm -> pipe1; pipe1 | parser -> chain
        mock_pipe1 = MagicMock()
        mock_rag_prompt.__or__.return_value = mock_pipe1
        mock_pipe1.__or__.return_value = mock_chain

        # Act
        gen = chat_service.process_message_stream(
            session_id=str(mock_session.id),
            user_message="Hello",
            db=mock_db,
        )

        events = []
        async for event_str in gen:
            events.append(json.loads(event_str))

        # Assert
        # Check Router Metadata
        meta_event = next((e for e in events if e["type"] == "metadata"), None)
        assert meta_event is not None
        assert meta_event["metadata"]["route"] == "rag"

        # Check Tokens
        tokens = [e["content"] for e in events if e["type"] == "token"]
        assert "chunk1" in tokens
        assert "chunk2" in tokens

        # Check Done
        assert any(e["type"] == "done" for e in events)

        # Verify calls
        mock_history.get_or_create_session.assert_awaited_once()
        mock_search.ainvoke.assert_awaited_once_with("Hello")
        # History updated twice: user message and assistant message
        assert mock_history.add_message.call_count == 2


@pytest.mark.asyncio
async def test_creates_new_session_if_none_provided(mock_db, mock_session):
    """Should create a new session if session_id is None."""
    mock_chain = AsyncMock()

    async def async_gen(*args, **kwargs):
        yield "chunk"

    mock_chain.astream = async_gen

    with (
        patch("app.services.chat_service.rag_prompt") as mock_rag_prompt,
        patch("app.services.chat_service.history_service") as mock_history,
        patch("app.services.chat_service.search_documents") as mock_search,
        patch("app.services.chat_service.get_router_agent") as mock_get_router,
    ):
        mock_history.get_or_create_session = AsyncMock(return_value=mock_session)
        mock_history.get_session_history = AsyncMock(return_value=[])
        mock_history.add_message = AsyncMock()

        mock_router_agent = AsyncMock()
        mock_router_agent.route.return_value.destination = "rag"
        mock_router_agent.route.return_value.reasoning = "test"
        mock_get_router.return_value = mock_router_agent

        mock_search.ainvoke = AsyncMock(return_value="")

        mock_pipe1 = MagicMock()
        mock_rag_prompt.__or__.return_value = mock_pipe1
        mock_pipe1.__or__.return_value = mock_chain

        # Act
        gen = chat_service.process_message_stream(
            session_id=None,
            user_message="Test",
            db=mock_db,
        )
        async for _ in gen:
            pass

        # Assert
        mock_history.get_or_create_session.assert_awaited_once_with(None, mock_db)
