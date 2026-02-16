"""FastAPI dependency injection providers."""

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import verify_api_key
from app.db.session import get_db_session


async def get_db(session: AsyncGenerator = Depends(get_db_session)) -> AsyncSession:
    """Provide a database session dependency."""
    return session


async def require_auth(api_key: str = Depends(verify_api_key)) -> str:
    """Require API key authentication."""
    return api_key
