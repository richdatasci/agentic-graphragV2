from graphrag_system.retrieval.graph_retriever import (
    SEARCH_TRIPLES,
    EvidenceFilter,
    GraphRetriever,
)
from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class GraphAgent:
    def __init__(self, retriever: GraphRetriever | None = None) -> None:
        self.retriever = retriever or GraphRetriever()

    def retrieve(
        self, query: str, top_k: int = 8, *, evidence_filter: EvidenceFilter | None = None,
    ) -> list[RetrievedEvidence]:
        return self.retriever.retrieve(query, top_k=top_k, evidence_filter=evidence_filter)

    def build_query(self, question: str) -> str:
        """Return a fixed template. Bind terms and limit separately as parameters."""
        return SEARCH_TRIPLES
