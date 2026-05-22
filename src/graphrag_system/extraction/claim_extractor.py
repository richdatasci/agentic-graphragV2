import re
from pydantic import BaseModel, Field

from graphrag_system.utils.hashing import stable_hash


class ExtractedClaim(BaseModel):
    id: str
    text: str
    confidence: float = 0.6
    metadata: dict = Field(default_factory=dict)


class ClaimExtractor:
    def extract(self, text: str) -> list[ExtractedClaim]:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if s.strip()]
        return [
            ExtractedClaim(id=f"claim_{stable_hash(sentence)[:12]}", text=sentence)
            for sentence in sentences
            if len(sentence.split()) >= 5
        ][:100]
