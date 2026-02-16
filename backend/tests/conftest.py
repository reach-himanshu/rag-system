"""Shared test fixtures for the RAG System backend."""

import pytest


@pytest.fixture
def api_key():
    """Test API key for authentication."""
    return "test-api-key"


@pytest.fixture
def auth_headers(api_key):
    """Headers with valid API key."""
    return {"X-API-Key": api_key}
