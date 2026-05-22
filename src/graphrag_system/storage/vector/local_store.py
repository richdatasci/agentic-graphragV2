import json
import math
from pathlib import Path

from graphrag_system.storage.vector.base import BaseVectorStore, VectorRecord


class LocalJsonVectorStore(BaseVectorStore):
    def __init__(self, path: str = ".local_data/vector_records.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, records: list[dict]) -> None:
        self.path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    def upsert(self, records: list[VectorRecord]) -> None:
        existing = {record["id"]: record for record in self._read()}
        for record in records:
            existing[record.id] = record.model_dump()
        self._write(list(existing.values()))

    def search(self, vector: list[float], top_k: int = 8) -> list[dict]:
        scored = []
        for record in self._read():
            score = self._cosine(vector, record["vector"])
            scored.append({"id": record["id"], "score": score, "payload": record})
        scored.sort(key=lambda row: row["score"], reverse=True)
        return scored[:top_k]

    def _cosine(self, a: list[float], b: list[float]) -> float:
        numerator = sum(x * y for x, y in zip(a, b))
        denom_a = math.sqrt(sum(x * x for x in a)) or 1.0
        denom_b = math.sqrt(sum(y * y for y in b)) or 1.0
        return numerator / (denom_a * denom_b)
