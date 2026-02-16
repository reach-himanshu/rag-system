"""API key authentication."""

from fastapi import Security
from fastapi.security import APIKeyHeader

from app.config import settings
from app.core.exceptions import AuthenticationError

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str | None = Security(api_key_header)) -> str:
    """Verify the API key from the request header."""
    if api_key is None or api_key != settings.api_key:
        raise AuthenticationError()
    return api_key
