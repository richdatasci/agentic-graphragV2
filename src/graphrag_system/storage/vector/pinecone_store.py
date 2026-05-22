from graphrag_system.storage.vector.base import BaseVectorStore, VectorRecord


class PineconeVectorStore(BaseVectorStore):
    def __init__(self, api_key: str = "INSERT API KEY HERE") -> None:
        self.api_key = api_key

    def upsert(self, records: list[VectorRecord]) -> None:
        return None

    def search(self, vector: list[float], top_k: int = 8) -> list[dict]:
        return []
