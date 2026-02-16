"""OpenAI embedding service for text vectorization."""

import logging

from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)

# Lazy-initialized client
_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    """Get or create the async OpenAI client."""
    global _client  # noqa: PLW0603
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _client


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a batch of texts.

    Args:
        texts: List of text strings to embed.

    Returns:
        List of embedding vectors (1536 dimensions for text-embedding-3-small).
    """
    if not texts:
        return []

    client = _get_client()

    # OpenAI supports batch embedding — send all at once
    response = await client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
    )

    embeddings = [item.embedding for item in response.data]
    logger.info(
        "Generated %d embeddings using %s (dims=%d)",
        len(embeddings),
        settings.openai_embedding_model,
        len(embeddings[0]) if embeddings else 0,
    )
    return embeddings


async def embed_query(text: str) -> list[float]:
    """Generate an embedding for a single query text.

    Args:
        text: Query text to embed.

    Returns:
        Embedding vector.
    """
    results = await embed_texts([text])
    return results[0]
