from pathlib import Path
from pydantic import BaseModel, Field

from graphrag_system.llm.embedding_gateway import EmbeddingGateway
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
    def __init__(self) -> None:
        self.embedder = EmbeddingGateway()
        self.store = LocalJsonVectorStore()

    def retrieve(self, query: str, top_k: int = 8) -> list[RetrievedEvidence]:
        if not Path(".local_data/vector_records.json").exists():
            return [
                RetrievedEvidence(
                    source_id="vector_placeholder",
                    chunk_id="chunk_placeholder",
                    title="Vector retrieval placeholder",
                    text=f"Vector retrieval is ready. Run `make ingest-sample` to index sample content. Query: {query}",
                    score=0.5,
                    source_type="vector",
                )
            ]
        query_vector = self.embedder.embed_text(query)
        results = self.store.search(query_vector, top_k=top_k)
        return [
            RetrievedEvidence(
                source_id=r["payload"].get("metadata", {}).get("document_id", r["id"]),
                chunk_id=r["id"],
                title=r["payload"].get("metadata", {}).get("title", "Indexed chunk"),
                text=r["payload"]["text"],
                score=float(r["score"]),
                source_type="vector",
                metadata=r["payload"].get("metadata", {}),
            )
            for r in results
        ]
