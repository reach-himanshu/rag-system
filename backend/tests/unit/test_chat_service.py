"""Unit tests for chat service RAG pipeline."""

import uuid
from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.api.v1.schemas.chat import MessageResponse
from app.db.models import ChatMessage, ChatSession
from app.services import chat_service


@pytest.fixture
def mock_db():
    """Create a mock async database session."""
    db = AsyncMock()
    return db


@pytest.fixture
def mock_session():
    """Create a mock ChatSession."""
    return ChatSession(id=uuid.uuid4())


@pytest.fixture
def mock_chain():
    """Create a mock LCEL chain."""
    chain = AsyncMock()
    chain.ainvoke.return_value = "This is the answer."
    return chain


class TestProcessMessage:
    """Tests for the process_message function."""

    @pytest.mark.asyncio
    @patch("app.services.chat_service.history_service")
    @patch("app.services.chat_service.search_documents")
    async def test_successful_rag_flow(
        self, mock_search, mock_history, mock_db, mock_session, mock_chain
    ):
        """Should execute full RAG flow: history -> search -> llm -> save."""
        # 1. Setup History
        # Ensure get_or_create_session is an AsyncMock that returns mock_session
        mock_history.get_or_create_session = AsyncMock(return_value=mock_session)
        
        # Configure add_message to return a dummy assistant message
        assistant_msg = ChatMessage(
            id=uuid.uuid4(),
            role="assistant",
            content="This is the answer.",
            route_decision="document_search",
            metadata_={"context_source": "document_search"},
            created_at=datetime.now(UTC)
        )
        mock_history.add_message = AsyncMock(return_value=assistant_msg)
        mock_history.get_session_history = AsyncMock(return_value=[])

        # 2. Setup Search Tool
        # Explicitly make ainvoke an AsyncMock so it can be awaited
        mock_search.ainvoke = AsyncMock(return_value="[Document 1] Context")

        # 3. Setup LLM Chain (patching the template | llm | parser pipeline)
        # In chat_service: chain = prompt_template | llm | StrOutputParser()
        # We patch prompt_template so that prompt_template | ... returns our mock chain
        with patch("app.services.chat_service.prompt_template") as mock_prompt_tmpl:
            # Mock the __or__ (pipe) behavior twice: prompt | llm -> pipe1 | parser -> chain
            mock_pipe1 = MagicMock()
            mock_prompt_tmpl.__or__.return_value = mock_pipe1
            mock_pipe1.__or__.return_value = mock_chain

            # Act
            response = await chat_service.process_message(
                session_id=str(mock_session.id),
                user_message="Hello",
                db=mock_db,
            )

            # Assert
            assert isinstance(response, MessageResponse)
            assert response.content == "This is the answer."
            assert response.route_decision == "document_search"
            
            # Verify calls
            mock_history.get_or_create_session.assert_awaited_once()
            assert mock_history.add_message.call_count == 2
            mock_search.ainvoke.assert_awaited_once_with("Hello")
            mock_chain.ainvoke.assert_awaited_once()

    @pytest.mark.asyncio
    @patch("app.services.chat_service.history_service")
    @patch("app.services.chat_service.search_documents")
    async def test_creates_new_session_if_none_provided(
        self, mock_search, mock_history, mock_db, mock_session, mock_chain
    ):
        """Should create a new session if session_id is None."""
        mock_history.get_or_create_session = AsyncMock(return_value=mock_session)
        mock_history.get_session_history = AsyncMock(return_value=[])
        mock_search.ainvoke = AsyncMock(return_value="")
        
        assistant_msg = ChatMessage(
            id=uuid.uuid4(),
            role="assistant",
            content="Answer",
            route_decision="document_search",
            metadata_={},
            created_at=datetime.now(UTC)
        )
        mock_history.add_message = AsyncMock(return_value=assistant_msg)

        with patch("app.services.chat_service.prompt_template") as mock_prompt_tmpl:
            mock_pipe1 = MagicMock()
            mock_prompt_tmpl.__or__.return_value = mock_pipe1
            mock_pipe1.__or__.return_value = mock_chain

            await chat_service.process_message(
                session_id=None,
                user_message="Test",
                db=mock_db,
            )

            mock_history.get_or_create_session.assert_awaited_once_with(None, mock_db)
