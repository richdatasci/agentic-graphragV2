import json
from pathlib import Path

from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class KeywordRetriever:
    def retrieve(self, query: str, top_k: int = 8) -> list[RetrievedEvidence]:
        path = Path(".local_data/chunks.json")
        if not path.exists():
            return [
                RetrievedEvidence(
                    source_id="keyword_placeholder",
                    title="Keyword retrieval placeholder",
                    text=f"Keyword retrieval is ready. Run `make ingest-sample` to index sample content. Query: {query}",
                    score=0.5,
                    source_type="keyword",
                )
            ][:top_k]

        chunks = json.loads(path.read_text(encoding="utf-8"))
        query_terms = set(query.lower().split())
        scored = []
        for chunk in chunks:
            text = chunk["text"]
            terms = set(text.lower().split())
            score = len(query_terms & terms) / max(len(query_terms), 1)
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
