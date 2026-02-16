"""Qdrant vector store wrapper for document storage and retrieval."""

import logging
import uuid
from dataclasses import dataclass

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import settings

logger = logging.getLogger(__name__)

# Lazy-initialized client
_client: QdrantClient | None = None

# text-embedding-3-small produces 1536-dimensional vectors
VECTOR_DIMENSION = 1536


@dataclass
class SearchResult:
    """A single vector search result."""

    text: str
    score: float
    document_id: str
    filename: str
    chunk_index: int


def _get_client() -> QdrantClient:
    """Get or create the Qdrant client."""
    global _client  # noqa: PLW0603
    if _client is None:
        _client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )
    return _client


def ensure_collection() -> None:
    """Create the Qdrant collection if it does not exist."""
    client = _get_client()
    collections = [c.name for c in client.get_collections().collections]

    if settings.qdrant_collection_name not in collections:
        client.create_collection(
            collection_name=settings.qdrant_collection_name,
            vectors_config=VectorParams(
                size=VECTOR_DIMENSION,
                distance=Distance.COSINE,
            ),
        )
        logger.info("Created Qdrant collection: %s", settings.qdrant_collection_name)
    else:
        logger.info("Qdrant collection already exists: %s", settings.qdrant_collection_name)


def upsert_chunks(
    document_id: str,
    chunks: list[dict],
    embeddings: list[list[float]],
) -> int:
    """Upsert document chunks with their embeddings into Qdrant.

    Args:
        document_id: UUID of the parent document.
        chunks: List of dicts with 'text', 'chunk_index', 'metadata' keys.
        embeddings: Corresponding embedding vectors.

    Returns:
        Number of points upserted.
    """
    client = _get_client()

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": chunk["text"],
                "document_id": document_id,
                "filename": chunk["metadata"].get("filename", ""),
                "chunk_index": chunk["chunk_index"],
                "total_chunks": chunk["metadata"].get("total_chunks", 0),
            },
        )
        for chunk, embedding in zip(chunks, embeddings, strict=True)
    ]

    # Qdrant supports batch upsert — send in batches of 100
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i : i + batch_size]
        client.upsert(
            collection_name=settings.qdrant_collection_name,
            points=batch,
        )

    logger.info(
        "Upserted %d chunks for document %s into Qdrant",
        len(points),
        document_id,
    )
    return len(points)


def search(query_embedding: list[float], top_k: int = 5) -> list[SearchResult]:
    """Search for similar chunks in Qdrant.

    Args:
        query_embedding: Query vector.
        top_k: Number of results to return.

    Returns:
        List of SearchResult objects ordered by relevance.
    """
    client = _get_client()

    results = client.query_points(
        collection_name=settings.qdrant_collection_name,
        query=query_embedding,
        limit=top_k,
    ).points

    return [
        SearchResult(
            text=hit.payload.get("text", ""),
            score=hit.score,
            document_id=hit.payload.get("document_id", ""),
            filename=hit.payload.get("filename", ""),
            chunk_index=hit.payload.get("chunk_index", 0),
        )
        for hit in results
    ]


def delete_by_document(document_id: str) -> None:
    """Delete all vectors belonging to a specific document.

    Args:
        document_id: UUID of the document whose vectors should be deleted.
    """
    from qdrant_client.models import FieldCondition, Filter, MatchValue

    client = _get_client()

    client.delete(
        collection_name=settings.qdrant_collection_name,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="document_id",
                    match=MatchValue(value=document_id),
                )
            ]
        ),
    )
    logger.info("Deleted vectors for document %s from Qdrant", document_id)
