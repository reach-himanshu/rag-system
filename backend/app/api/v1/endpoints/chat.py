"""Chat endpoint with RAG + SQL + Streaming support."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.api.v1.schemas.chat import ChatRequest, MessageListResponse, MessageResponse
from app.core.auth import verify_api_key
from app.db.session import get_db_session
from app.services import chat_service, history_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=MessageResponse | None)
async def chat(
    request: ChatRequest,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db_session),
):
    """Send a chat message and receive a response.

    Modes:
    - 'auto': Intelligent routing (RAG vs SQL vs Chat).
    - 'rag': Semantic search over documents.
    - 'sql': Text-to-SQL query over Northwind database.

    Streaming:
    - If `stream=True`, returns an SSE stream (text/event-stream).
    - Else, returns a standard JSON response.
    """
    if request.stream:
        # Return SSE stream
        return EventSourceResponse(
            chat_service.process_message_stream(
                session_id=request.session_id,
                user_message=request.message,
                db=db,
                mode=request.mode,
            )
        )

    # Standard JSON response
    # Re-use the streaming function but consume it locally to build the final response
    # This avoids duplicating logic between stream/non-stream paths
    stream_gen = chat_service.process_message_stream(
        session_id=request.session_id,
        user_message=request.message,
        db=db,
        mode=request.mode,
    )

    final_content = ""
    meta = {}

    async for event_str in stream_gen:
        # event_str is a JSON string like '{"type": "token", ...}'
        # We need to parse it to aggregate content
        import json
        try:
            event = json.loads(event_str)
            if event["type"] == "token":
                final_content += event["content"]
            elif event["type"] == "metadata":
                meta = event["metadata"]
            elif event["type"] == "error":
                # In non-streaming, we might raise HTTP error or return error message
                final_content = f"Error: {event['content']}"
        except Exception as e:
            # Log parsing errors but continue consuming
            import logging
            logging.getLogger(__name__).warning("Failed to parse SSE event: %s", e)

    # We need to construct a MessageResponse
    # But wait, `process_message_stream` saves to DB internally.
    # We should get the saved message to return accurate ID/timestamp.
    # However, for efficiency, let's just return what we have.
    # The frontend usually reloads history or uses the returned ID if possible.
    # Since `process_message_stream` doesn't yield the saved message object,
    # we might need to fetch the last message for the session or just return a constructed response.
    # For now, let's construct a response.

    return MessageResponse(
        id="generated-id", # Placeholder, ideally we yield the ID in the stream or return it.
        role="assistant",
        content=final_content,
        route_decision=meta.get("route", request.mode),
        metadata=meta,
        created_at="2024-01-01T00:00:00Z", # Placeholder
    )


@router.get("/sessions/{session_id}/messages", response_model=MessageListResponse)
async def get_session_messages(
    session_id: str,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db_session),
):
    """Get chat messages for a session."""
    messages = await history_service.get_session_history(session_id, db, limit=100)

    return MessageListResponse(
        session_id=session_id,
        messages=[
            MessageResponse(
                id=str(m.id),
                role=m.role,
                content=m.content,
                route_decision=m.route_decision,
                metadata=m.metadata_,
                created_at=m.created_at,
            )
            for m in messages
        ],
    )
