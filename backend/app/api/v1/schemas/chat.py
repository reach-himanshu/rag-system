"""Chat request/response schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str = Field(..., min_length=1, max_length=4000)
    mode: str = Field(
        default="auto",
        description="Processing mode: 'auto', 'rag', or 'sql'.",
    )
    stream: bool = Field(
        default=False,
        description="Whether to stream the response (SSE).",
    )


class ChatResponseChunk(BaseModel):
    type: Literal["token", "metadata", "done", "error"]
    content: str | None = None
    metadata: dict | None = None


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    route_decision: str | None = None
    metadata: dict | None = None
    created_at: datetime


class MessageListResponse(BaseModel):
    session_id: str
    messages: list[MessageResponse]
