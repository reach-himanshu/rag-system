from qdrant_client import QdrantClient
print("Available methods in QdrantClient:")
client = QdrantClient(":memory:")
print([m for m in dir(client) if not m.startswith("_")])
print(f"Has search: {'search' in dir(client)}")
