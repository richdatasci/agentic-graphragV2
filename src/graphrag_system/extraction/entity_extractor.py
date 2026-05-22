import re
from pydantic import BaseModel, Field

from graphrag_system.utils.hashing import stable_hash


class ExtractedEntity(BaseModel):
    id: str
    name: str
    label: str = "Entity"
    confidence: float = 0.6
    metadata: dict = Field(default_factory=dict)


class EntityExtractor:
    """Simple deterministic extractor. Replace with LLM extraction when ready."""

    ENTITY_PATTERN = re.compile(r"\b[A-Z][A-Za-z0-9_\-]*(?:\s+[A-Z][A-Za-z0-9_\-]*){0,4}\b")

    def extract(self, text: str) -> list[ExtractedEntity]:
        seen: set[str] = set()
        entities: list[ExtractedEntity] = []
        for match in self.ENTITY_PATTERN.finditer(text or ""):
            name = match.group(0).strip()
            if len(name) < 3 or name in seen:
                continue
            seen.add(name)
            entities.append(ExtractedEntity(id=f"ent_{stable_hash(name)[:12]}", name=name))
        return entities[:100]
