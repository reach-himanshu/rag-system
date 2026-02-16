"""API v1 router aggregating all endpoint routers."""

from fastapi import APIRouter

from app.api.v1.endpoints import chat, documents, health

api_router = APIRouter()

# Health check (no auth required)
api_router.include_router(health.router, tags=["health"])

# Authenticated endpoints
api_router.include_router(documents.router, prefix="/api/v1")
api_router.include_router(chat.router, prefix="/api/v1")
