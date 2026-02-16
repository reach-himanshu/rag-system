"""Document search tool for the RAG agent."""

import logging

from langchain_core.tools import tool

from app.services import embedding_service, vector_store

logger = logging.getLogger(__name__)


@tool
async def search_documents(query: str) -> str:
    """Search for relevant documents using semantic search.

    Args:
        query: The user's question or search query.

    Returns:
        A formatted string containing relevant document chunks and their metadata.
    """
    try:
        # Generate embedding for the query
        query_vector = await embedding_service.embed_query(query)

        # Search Qdrant
        results = vector_store.search(query_vector, top_k=5)

        if not results:
            return "No relevant documents found."

        # Format results for the LLM
        context_parts = []
        for i, res in enumerate(results, 1):
            context_parts.append(
                f"[Document {i}: {res.filename} (Score: {res.score:.2f})]\n{res.text}"
            )

        return "\n\n".join(context_parts)

    except Exception as e:
        logger.exception("Document search failed: %s", e)
        return f"Error searching documents: {e}"
