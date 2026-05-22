from graphrag_system.storage.vector.base import BaseVectorStore, VectorRecord


class QdrantVectorStore(BaseVectorStore):
    def __init__(
        self,
        url: str = "http://localhost:6333",
        collection_name: str = "documents",
        api_key: str = "INSERT API KEY HERE",
    ) -> None:
        self.url = url
        self.collection_name = collection_name
        self.api_key = api_key
        try:
            from qdrant_client import QdrantClient

            self.client = QdrantClient(url=url, api_key=None if api_key == "INSERT API KEY HERE" else api_key)
        except Exception:
            self.client = None

    def upsert(self, records: list[VectorRecord]) -> None:
        if not self.client or not records:
            return
        from qdrant_client.models import PointStruct

        points = [
            PointStruct(id=record.id, vector=record.vector, payload={"text": record.text, **record.metadata})
            for record in records
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, vector: list[float], top_k: int = 8) -> list[dict]:
        if not self.client:
            return []
        try:
            results = self.client.search(collection_name=self.collection_name, query_vector=vector, limit=top_k)
        except Exception:
            try:
                results = self.client.query_points(collection_name=self.collection_name, query=vector, limit=top_k).points
            except Exception:
                return []
        return [{"id": str(r.id), "score": r.score, "payload": r.payload} for r in results]
