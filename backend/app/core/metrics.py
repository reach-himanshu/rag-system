"""Prometheus metrics for the RAG System."""

from prometheus_client import Counter, Histogram

# Request metrics (auto-instrumented by prometheus-fastapi-instrumentator)
# These are custom application-level metrics:

documents_processed_total = Counter(
    "rag_documents_processed_total",
    "Total number of documents processed",
    ["status"],  # success, error
)

rag_queries_total = Counter(
    "rag_queries_total",
    "Total number of RAG queries",
    ["route"],  # document_search, sql_query, both
)

llm_latency_seconds = Histogram(
    "rag_llm_latency_seconds",
    "LLM call latency in seconds",
    ["operation"],  # embed, chat, route, sql
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
)
