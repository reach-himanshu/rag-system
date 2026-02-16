"""Unit tests for document text chunker."""

from app.document_processing.chunker import CHUNK_OVERLAP, CHUNK_SIZE, TextChunk, chunk_text


class TestChunkText:
    """Tests for the chunk_text function."""

    def test_empty_text_returns_empty_list(self):
        """Should return empty list for empty or whitespace-only text."""
        result = chunk_text("", "doc-1", "empty.pdf")
        assert result == []

        result = chunk_text("   \n\n  ", "doc-1", "whitespace.pdf")
        assert result == []

    def test_short_text_returns_single_chunk(self):
        """Text shorter than chunk_size should produce a single chunk."""
        text = "This is a short document."
        chunks = chunk_text(text, "doc-1", "short.pdf")

        assert len(chunks) == 1
        assert chunks[0].text == text
        assert chunks[0].chunk_index == 0

    def test_long_text_produces_multiple_chunks(self):
        """Text longer than chunk_size should be split into multiple chunks."""
        # Create text that is significantly longer than CHUNK_SIZE
        text = "This is a sentence about topic A. " * 200  # ~6800 chars
        chunks = chunk_text(text, "doc-1", "long.pdf")

        assert len(chunks) > 1
        # All chunks should have sequential indices
        for i, chunk in enumerate(chunks):
            assert chunk.chunk_index == i

    def test_chunks_have_correct_metadata(self):
        """Each chunk should carry document metadata."""
        text = "Some test content. " * 300
        doc_id = "abc-123"
        filename = "report.pdf"

        chunks = chunk_text(text, doc_id, filename)

        for chunk in chunks:
            assert chunk.metadata["document_id"] == doc_id
            assert chunk.metadata["filename"] == filename
            assert chunk.metadata["total_chunks"] == len(chunks)
            assert chunk.metadata["chunk_index"] == chunk.chunk_index

    def test_chunk_returns_text_chunk_dataclass(self):
        """Return type should be list of TextChunk dataclass instances."""
        chunks = chunk_text("Some content here.", "doc-1", "file.pdf")
        assert len(chunks) == 1
        assert isinstance(chunks[0], TextChunk)
        assert hasattr(chunks[0], "text")
        assert hasattr(chunks[0], "chunk_index")
        assert hasattr(chunks[0], "metadata")

    def test_custom_chunk_size(self):
        """Should respect custom chunk_size parameter."""
        text = "Word " * 500  # 2500 chars
        small_chunks = chunk_text(text, "doc-1", "file.pdf", chunk_size=100, chunk_overlap=10)
        large_chunks = chunk_text(text, "doc-1", "file.pdf", chunk_size=1000, chunk_overlap=10)

        assert len(small_chunks) > len(large_chunks)

    def test_default_parameters_match_constants(self):
        """Default chunk_size and chunk_overlap should match module constants."""
        assert CHUNK_SIZE == 2048
        assert CHUNK_OVERLAP == 200
