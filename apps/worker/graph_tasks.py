from typing import Any

from apps.worker.celery_app import celery_app
from graphrag_system.extraction.entity_extractor import EntityExtractor
from graphrag_system.extraction.relationship_extractor import RelationshipExtractor
from graphrag_system.extraction.triple_extractor import TripleExtractor


@celery_app.task(name="apps.worker.graph_tasks.extract_graph_from_document", bind=True)
def extract_graph_from_document(self, document_id: str, text: str = "", options: dict[str, Any] | None = None) -> dict[str, Any]:
    entities = EntityExtractor().extract(text)
    relationships = RelationshipExtractor().extract(text, entities)
    triples = TripleExtractor().extract(text, entities, relationships)
    return {
        "task_id": self.request.id,
        "status": "completed",
        "document_id": document_id,
        "entities": [e.model_dump() for e in entities],
        "relationships": [r.model_dump() for r in relationships],
        "triples": [t.model_dump() for t in triples],
    }


@celery_app.task(name="apps.worker.graph_tasks.index_graph_triples", bind=True)
def index_graph_triples(self, document_id: str | None = None) -> dict[str, Any]:
    return {"task_id": self.request.id, "status": "completed", "document_id": document_id}
