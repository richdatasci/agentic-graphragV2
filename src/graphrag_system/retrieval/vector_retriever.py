from pydantic import BaseModel, Field

from graphrag_system.llm.embedding_gateway import EmbeddingGateway
from graphrag_system.storage.vector.base import BaseVectorStore
from graphrag_system.storage.vector.local_store import LocalJsonVectorStore


class RetrievedEvidence(BaseModel):
    source_id: str
    chunk_id: str | None = None
    title: str | None = None
    text: str
    score: float | None = None
    source_type: str
    metadata: dict = Field(default_factory=dict)


class VectorRetriever:
    def __init__(
        self, store: BaseVectorStore | None = None, embedder: EmbeddingGateway | None = None,
    ) -> None:
        self.embedder = embedder or EmbeddingGateway()
        self.store = store or LocalJsonVectorStore()

    def retrieve(self, query: str, top_k: int = 8) -> list[RetrievedEvidence]:
        if isinstance(self.store, LocalJsonVectorStore) and not self.store.path.exists():
            return []
        query_vector = self.embedder.embed_text(query)
        results = self.store.search(query_vector, top_k=top_k)
        evidence = []
        for row in results:
            payload = row["payload"] or {}
            if not isinstance(payload.get("text"), str) or not row["score"] > 0:
                continue
            metadata = payload.get("metadata")
            if not isinstance(metadata, dict):
                metadata = payload
            evidence.append(RetrievedEvidence(
                source_id=metadata.get("document_id") or row["id"],
                chunk_id=metadata.get("chunk_id") or row["id"],
                title=metadata.get("title") or "Indexed chunk",
                text=payload["text"],
                score=float(row["score"]),
                source_type="vector",
                metadata=metadata,
            ))
        return evidence
