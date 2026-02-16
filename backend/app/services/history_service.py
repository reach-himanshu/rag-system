"""Service for managing chat history in PostgreSQL."""

import logging
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import ChatMessage, ChatSession

logger = logging.getLogger(__name__)


async def get_or_create_session(session_id: str | None, db: AsyncSession) -> ChatSession:
    """Get an existing chat session or create a new one.

    Args:
        session_id: UUID string of the session, or None to create new.
        db: Async database session.

    Returns:
        The ChatSession ORM object.
    """
    if session_id:
        try:
            session_uuid = uuid.UUID(session_id)
            stmt = select(ChatSession).options(
                selectinload(ChatSession.messages)
            ).where(ChatSession.id == session_uuid)
            result = await db.execute(stmt)
            session = result.scalars().first()
            if session:
                return session
            logger.warning("Session %s not found, creating new one", session_id)
        except ValueError:
            logger.warning("Invalid session ID %s, creating new one", session_id)

    # Create new session
    session = ChatSession(id=uuid.uuid4())
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def add_message(
    session_id: uuid.UUID,
    role: str,
    content: str,
    db: AsyncSession,
    metadata: dict | None = None,
    route_decision: str | None = None,
) -> ChatMessage:
    """Add a message to the chat history.

    Args:
        session_id: UUID of the session.
        role: 'user' or 'assistant'.
        content: Message content.
        db: Async database session.
        metadata: Optional JSON metadata (e.g., sources).
        route_decision: Optional routing decision tag.

    Returns:
        The created ChatMessage ORM object.
    """
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        metadata_=metadata,
        route_decision=route_decision,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def get_session_history(
    session_id: str,
    db: AsyncSession,
    limit: int = 10,
) -> list[ChatMessage]:
    """Get recent messages for a session.

    Args:
        session_id: UUID string.
        db: Async database session.
        limit: Number of recent messages to retrieve.

    Returns:
        List of ChatMessage objects (newest last).
    """
    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        return []

    stmt = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_uuid)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    messages = result.scalars().all()
    return sorted(messages, key=lambda m: m.created_at)
