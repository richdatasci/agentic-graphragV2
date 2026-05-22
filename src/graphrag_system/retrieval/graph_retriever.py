import json
from pathlib import Path

from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class GraphRetriever:
    def retrieve(self, query: str, top_k: int = 8) -> list[RetrievedEvidence]:
        path = Path(".local_data/triples.json")
        if not path.exists():
            return [
                RetrievedEvidence(
                    source_id="graph_placeholder",
                    title="Graph retrieval placeholder",
                    text=f"Graph retrieval is ready. Run `make ingest-sample` to create local triples. Query: {query}",
                    score=0.5,
                    source_type="graph",
                )
            ][:top_k]

        triples = json.loads(path.read_text(encoding="utf-8"))
        query_terms = set(query.lower().split())
        scored = []
        for triple in triples:
            text = f"{triple['subject']} {triple['predicate']} {triple['object']}"
            terms = set(text.lower().split())
            score = len(query_terms & terms) / max(len(query_terms), 1)
            scored.append((score, triple, text))
        scored.sort(key=lambda item: item[0], reverse=True)

        return [
            RetrievedEvidence(
                source_id=triple.get("source_document_id", "local_graph"),
                title="Local graph triple",
                text=text,
                score=score,
                source_type="graph",
                metadata=triple,
            )
            for score, triple, text in scored[:top_k]
        ]
