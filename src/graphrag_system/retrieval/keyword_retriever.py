import json
import re
from pathlib import Path

from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class KeywordRetriever:
    def retrieve(self, query: str, top_k: int = 8) -> list[RetrievedEvidence]:
        path = Path(".local_data/chunks.json")
        if not path.exists():
            return []
        chunks = json.loads(path.read_text(encoding="utf-8"))
        query_terms = set(re.findall(r"\w+", query.casefold()))
        scored = []
        for chunk in chunks:
            text = chunk["text"]
            terms = set(re.findall(r"\w+", text.casefold()))
            score = len(query_terms & terms) / max(len(query_terms), 1)
            if not score:
                continue
            scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)

        return [
            RetrievedEvidence(
                source_id=chunk.get("document_id", "local"),
                chunk_id=chunk["id"],
                title=chunk.get("metadata", {}).get("title", "Local chunk"),
                text=chunk["text"],
                score=score,
                source_type="keyword",
                metadata=chunk.get("metadata", {}),
            )
            for score, chunk in scored[:top_k]
        ]
