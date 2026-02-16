"""Health check endpoint."""

from fastapi import APIRouter

from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Return application health status."""
    return {
        "status": "ok",
        "version": settings.app_version,
        "service": settings.app_name,
    }
