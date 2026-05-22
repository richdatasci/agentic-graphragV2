from pydantic import BaseModel, Field

from graphrag_system.extraction.entity_extractor import ExtractedEntity
from graphrag_system.extraction.relationship_extractor import ExtractedRelationship
from graphrag_system.utils.hashing import stable_hash


class ExtractedTriple(BaseModel):
    id: str
    subject: str
    predicate: str
    object: str
    confidence: float = 0.5
    metadata: dict = Field(default_factory=dict)


class TripleExtractor:
    def extract(
        self,
        text: str,
        entities: list[ExtractedEntity],
        relationships: list[ExtractedRelationship],
    ) -> list[ExtractedTriple]:
        by_id = {entity.id: entity for entity in entities}
        triples: list[ExtractedTriple] = []
        for rel in relationships:
            source = by_id.get(rel.source_entity_id)
            target = by_id.get(rel.target_entity_id)
            if not source or not target:
                continue
            key = f"{source.name}:{rel.type}:{target.name}"
            triples.append(
                ExtractedTriple(
                    id=f"triple_{stable_hash(key)[:12]}",
                    subject=source.name,
                    predicate=rel.type,
                    object=target.name,
                    confidence=rel.confidence,
                )
            )
        return triples
