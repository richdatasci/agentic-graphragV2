from graphrag_system.storage.vector.base import BaseVectorStore, VectorRecord


class WeaviateVectorStore(BaseVectorStore):
    def upsert(self, records: list[VectorRecord]) -> None:
        return None

    def search(self, vector: list[float], top_k: int = 8) -> list[dict]:
        return []
