from typing import Any

from apps.worker.celery_app import celery_app
from graphrag_system.storage.vector.base import VectorRecord
from graphrag_system.storage.vector.qdrant_store import QdrantVectorStore


@celery_app.task(name="apps.worker.embedding_tasks.embed_document_chunks", bind=True)
def embed_document_chunks(self, document_id: str, chunk_ids: list[str] | None = None) -> dict[str, Any]:
    return {
        "task_id": self.request.id,
        "status": "accepted",
        "stage": "embedding",
        "document_id": document_id,
        "chunk_ids": chunk_ids or [],
        "message": "Wire this to the embedding model once chunks are persisted.",
    }


@celery_app.task(name="apps.worker.embedding_tasks.upsert_vector_records", bind=True)
def upsert_vector_records(self, collection: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    vector_store = QdrantVectorStore(collection_name=collection)
    parsed = [VectorRecord(**r) for r in records]
    vector_store.upsert(parsed)
    return {"task_id": self.request.id, "status": "completed", "records": len(records)}
