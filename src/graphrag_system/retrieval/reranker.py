from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class Reranker:
    def rerank(self, query: str, evidence: list[RetrievedEvidence]) -> list[RetrievedEvidence]:
        return sorted(evidence, key=lambda item: item.score or 0.0, reverse=True)
