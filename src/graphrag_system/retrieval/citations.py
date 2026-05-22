from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class CitationBuilder:
    def build(self, evidence: list[RetrievedEvidence]) -> list[dict]:
        return [
            {
                "source_id": item.source_id,
                "chunk_id": item.chunk_id,
                "title": item.title,
                "score": item.score,
                "source_type": item.source_type,
            }
            for item in evidence
        ]
