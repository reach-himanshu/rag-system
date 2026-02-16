"""Document service — orchestrates the ingestion pipeline."""

import logging
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DocumentProcessingError, NotFoundError
from app.db.models import Document
from app.document_processing.chunker import chunk_text
from app.document_processing.extractors import SUPPORTED_TYPES, extract_text
from app.services import embedding_service, vector_store

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


async def process_document(
    filename: str,
    content_type: str,
    file_bytes: bytes,
    db: AsyncSession,
) -> Document:
    """Process an uploaded document through the full ingestion pipeline.

    Pipeline: validate → save metadata → extract → chunk → embed → store vectors → update status.

    Args:
        filename: Original filename.
        content_type: MIME type.
        file_bytes: Raw file content.
        db: Async database session.

    Returns:
        The Document ORM object with final status.

    Raises:
        DocumentProcessingError: If validation or processing fails.
    """
    # 1. Validate
    if content_type not in SUPPORTED_TYPES:
        raise DocumentProcessingError(
            f"Unsupported file type: {content_type}. Supported: {', '.join(SUPPORTED_TYPES.keys())}"
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise DocumentProcessingError(
            f"File size ({len(file_bytes)} bytes) exceeds maximum ({MAX_FILE_SIZE} bytes)"
        )

    if len(file_bytes) == 0:
        raise DocumentProcessingError("File is empty")

    # 2. Save metadata to PostgreSQL (status = "processing")
    doc = Document(
        id=uuid.uuid4(),
        filename=filename,
        file_type=SUPPORTED_TYPES[content_type],
        file_size_bytes=len(file_bytes),
        status="processing",
    )
    db.add(doc)
    await db.flush()  # Get the ID without committing

    doc_id = str(doc.id)
    logger.info("Processing document %s (%s, %d bytes)", doc_id, filename, len(file_bytes))

    try:
        # 3. Extract text
        text = extract_text(file_bytes, content_type)
        logger.info("Extracted %d chars from %s", len(text), filename)

        # 4. Chunk
        chunks = chunk_text(text, doc_id, filename)
        logger.info("Created %d chunks from %s", len(chunks), filename)

        # 5. Embed
        chunk_texts = [c.text for c in chunks]
        embeddings = await embedding_service.embed_texts(chunk_texts)

        # 6. Ensure Qdrant collection exists, then upsert vectors
        vector_store.ensure_collection()
        chunk_dicts = [
            {"text": c.text, "chunk_index": c.chunk_index, "metadata": c.metadata} for c in chunks
        ]
        vector_store.upsert_chunks(doc_id, chunk_dicts, embeddings)

        # 7. Update status to "ready"
        doc.status = "ready"
        doc.chunk_count = len(chunks)
        logger.info("Document %s processed successfully (%d chunks)", doc_id, len(chunks))

    except DocumentProcessingError:
        doc.status = "error"
        doc.error_message = "Document processing failed"
        raise
    except Exception as e:
        doc.status = "error"
        doc.error_message = str(e)
        logger.exception("Failed to process document %s: %s", doc_id, e)
        raise DocumentProcessingError(f"Processing failed: {e}") from e

    return doc


async def list_documents(db: AsyncSession) -> list[Document]:
    """List all uploaded documents.

    Args:
        db: Async database session.

    Returns:
        List of Document ORM objects ordered by creation time (newest first).
    """
    result = await db.execute(select(Document).order_by(Document.created_at.desc()))
    return list(result.scalars().all())


async def get_document(document_id: str, db: AsyncSession) -> Document:
    """Get a document by ID.

    Args:
        document_id: UUID string.
        db: Async database session.

    Returns:
        Document ORM object.

    Raises:
        NotFoundError: If document does not exist.
    """
    doc = await db.get(Document, uuid.UUID(document_id))
    if doc is None:
        raise NotFoundError("Document", document_id)
    return doc


async def delete_document(document_id: str, db: AsyncSession) -> None:
    """Delete a document and its vectors.

    Args:
        document_id: UUID string.
        db: Async database session.

    Raises:
        NotFoundError: If document does not exist.
    """
    doc = await get_document(document_id, db)

    # Delete vectors from Qdrant
    try:
        vector_store.delete_by_document(document_id)
    except Exception:
        logger.warning("Failed to delete vectors for document %s (may not exist)", document_id)

    # Delete from PostgreSQL
    await db.delete(doc)
    logger.info("Deleted document %s (%s)", document_id, doc.filename)
