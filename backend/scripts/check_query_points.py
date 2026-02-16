from qdrant_client import QdrantClient
client = QdrantClient(":memory:")
print(f"Has query_points: {hasattr(client, 'query_points')}")
