from pydantic import BaseModel, Field

from graphrag_system.extraction.entity_extractor import ExtractedEntity
from graphrag_system.utils.hashing import stable_hash


class ExtractedRelationship(BaseModel):
    id: str
    source_entity_id: str
    target_entity_id: str
    type: str = "RELATED_TO"
    confidence: float = 0.5
    metadata: dict = Field(default_factory=dict)


class RelationshipExtractor:
    """Creates co-occurrence relationships as a safe baseline."""

    def extract(self, text: str, entities: list[ExtractedEntity]) -> list[ExtractedRelationship]:
        relationships: list[ExtractedRelationship] = []
        for idx, source in enumerate(entities[:-1]):
            target = entities[idx + 1]
            rel_key = f"{source.id}:{target.id}:RELATED_TO"
            relationships.append(
                ExtractedRelationship(
                    id=f"rel_{stable_hash(rel_key)[:12]}",
                    source_entity_id=source.id,
                    target_entity_id=target.id,
                )
            )
        return relationships[:100]
