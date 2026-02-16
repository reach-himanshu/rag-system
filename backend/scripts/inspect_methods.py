from qdrant_client import QdrantClient
client = QdrantClient(":memory:")
methods = [m for m in dir(client) if "query" in m or "search" in m]
print(f"Search/Query methods: {methods}")
