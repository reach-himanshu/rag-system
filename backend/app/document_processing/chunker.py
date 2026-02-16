"""Document text chunking using LangChain's RecursiveCharacterTextSplitter."""

import logging
from dataclasses import dataclass, field

from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

# Design decision: 512 tokens (~2048 chars), 50 token overlap (~200 chars)
# Per FloTorch benchmarks, this balances accuracy and context.
CHUNK_SIZE = 2048  # approximate chars for ~512 tokens
CHUNK_OVERLAP = 200  # approximate chars for ~50 tokens


@dataclass
class TextChunk:
    """A chunk of text with positional metadata."""

    text: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)


def chunk_text(
    text: str,
    document_id: str,
    filename: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[TextChunk]:
    """Split text into overlapping chunks with metadata.

    Args:
        text: Full document text to chunk.
        document_id: UUID of the parent document.
        filename: Original filename for metadata.
        chunk_size: Maximum chunk size in characters.
        chunk_overlap: Overlap between consecutive chunks in characters.

    Returns:
        List of TextChunk objects with positional metadata.
    """
    if not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    raw_chunks = splitter.split_text(text)

    chunks = [
        TextChunk(
            text=chunk_text_content,
            chunk_index=i,
            metadata={
                "document_id": document_id,
                "filename": filename,
                "chunk_index": i,
                "total_chunks": len(raw_chunks),
            },
        )
        for i, chunk_text_content in enumerate(raw_chunks)
    ]

    logger.info(
        "Chunked document %s into %d chunks (avg %d chars)",
        filename,
        len(chunks),
        sum(len(c.text) for c in chunks) // max(len(chunks), 1),
    )
    return chunks
