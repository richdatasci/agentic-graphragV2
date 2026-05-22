from typing import Any

from apps.worker.celery_app import celery_app
from graphrag_system.ingestion.pipeline import IngestionPipeline


@celery_app.task(name="apps.worker.ingestion_tasks.ingest_source", bind=True)
def ingest_source(self, source_payload: dict[str, Any]) -> dict[str, Any]:
    pipeline = IngestionPipeline()
    result = pipeline.ingest_source(source_payload)
    result["task_id"] = self.request.id
    return result


@celery_app.task(name="apps.worker.ingestion_tasks.ingest_uploaded_file", bind=True)
def ingest_uploaded_file(self, file_payload: dict[str, Any]) -> dict[str, Any]:
    pipeline = IngestionPipeline()
    result = pipeline.ingest_uploaded_file(file_payload)
    result["task_id"] = self.request.id
    return result


@celery_app.task(name="apps.worker.ingestion_tasks.reprocess_document", bind=True)
def reprocess_document(self, document_id: str, options: dict[str, Any] | None = None) -> dict[str, Any]:
    pipeline = IngestionPipeline()
    result = pipeline.reprocess_document(document_id, options or {})
    result["task_id"] = self.request.id
    return result
