import json
from pathlib import Path

try:
    from rapidfuzz import fuzz
except Exception:
    fuzz = None

SAMPLE_TRIPLES = [
    {
        "id": "triple_001",
        "subject": "Agentic GraphRAG",
        "predicate": "combines",
        "object": "graph retrieval and vector search",
        "confidence": 0.91,
        "source_document_id": "doc_architecture",
        "chunk_id": "chunk_001",
        "metadata": {},
    },
    {
        "id": "triple_002",
        "subject": "Faithfulness evaluation",
        "predicate": "checks",
        "object": "answer support against retrieved context",
        "confidence": 0.89,
        "source_document_id": "doc_architecture",
        "chunk_id": "chunk_002",
        "metadata": {},
    },
]


class TriplePreviewService:
    def __init__(self, triples: list[dict] | None = None) -> None:
        if triples is not None:
            self.triples = triples
        elif Path(".local_data/triples.json").exists():
            self.triples = json.loads(Path(".local_data/triples.json").read_text(encoding="utf-8"))
        else:
            self.triples = SAMPLE_TRIPLES

    def search(self, query: str, limit: int = 25, min_confidence: float | None = None) -> list[dict]:
        scored = []
        for triple in self.triples:
            if min_confidence is not None and (triple.get("confidence") or 0) < min_confidence:
                continue
            haystack = f"{triple['subject']} {triple['predicate']} {triple['object']}"
            score = self._score(query, haystack)
            scored.append((score, triple))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [triple for _, triple in scored[:limit]]

    def _score(self, query: str, haystack: str) -> float:
        if fuzz:
            return float(fuzz.partial_ratio(query.lower(), haystack.lower()))
        query_terms = set(query.lower().split())
        hay_terms = set(haystack.lower().split())
        return 100.0 * len(query_terms & hay_terms) / max(len(query_terms), 1)
