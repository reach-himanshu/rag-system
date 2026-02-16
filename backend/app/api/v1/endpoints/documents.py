"""Document upload and management endpoints."""

import logging

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.documents import DocumentListResponse, DocumentResponse, UploadResponse
from app.core.auth import verify_api_key
from app.core.exceptions import DocumentProcessingError
from app.db.session import get_db_session
from app.services import document_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db_session),
):
    """Upload a document for processing.

    Accepts PDF, Word, Excel, and PowerPoint files up to 50MB.
    The document is processed asynchronously: extracted, chunked, embedded, and stored.
    """
    # Validate content type
    if file.content_type not in ALLOWED_TYPES:
        raise DocumentProcessingError(
            f"Unsupported file type: {file.content_type}. Supported: PDF, Word, Excel, PowerPoint"
        )

    # Read file bytes
    file_bytes = await file.read()

    # Validate size
    if len(file_bytes) > MAX_FILE_SIZE:
        raise DocumentProcessingError(
            f"File too large ({len(file_bytes)} bytes). Maximum: {MAX_FILE_SIZE} bytes"
        )

    # Process through the ingestion pipeline
    doc = await document_service.process_document(
        filename=file.filename or "untitled",
        content_type=file.content_type,
        file_bytes=file_bytes,
        db=db,
    )

    return UploadResponse(
        document_id=str(doc.id),
        filename=doc.filename,
        status=doc.status,
        message=f"Document processed: {doc.chunk_count} chunks created",
    )


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db_session),
):
    """List all uploaded documents."""
    docs = await document_service.list_documents(db)
    return DocumentListResponse(
        documents=[
            DocumentResponse(
                id=str(d.id),
                filename=d.filename,
                file_type=d.file_type,
                file_size_bytes=d.file_size_bytes,
                chunk_count=d.chunk_count,
                status=d.status,
                error_message=d.error_message,
                created_at=d.created_at,
                updated_at=d.updated_at,
            )
            for d in docs
        ],
        total=len(docs),
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db_session),
):
    """Get details for a specific document."""
    doc = await document_service.get_document(document_id, db)
    return DocumentResponse(
        id=str(doc.id),
        filename=doc.filename,
        file_type=doc.file_type,
        file_size_bytes=doc.file_size_bytes,
        chunk_count=doc.chunk_count,
        status=doc.status,
        error_message=doc.error_message,
        created_at=doc.created_at,
        updated_at=doc.updated_at,
    )


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    _api_key: str = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db_session),
):
    """Delete a document and its vector embeddings."""
    await document_service.delete_document(document_id, db)
    return {"message": f"Document {document_id} deleted"}
