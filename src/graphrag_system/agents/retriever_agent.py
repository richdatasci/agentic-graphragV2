from graphrag_system.agents.state import DecisionPoint
from graphrag_system.retrieval.hybrid_retriever import HybridRetriever
from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class RetrieverAgent:
    def __init__(self, retriever: HybridRetriever | None = None) -> None:
        self.retriever = retriever or HybridRetriever()

    async def retrieve(self, query: str) -> tuple[list[RetrievedEvidence], str, DecisionPoint]:
        evidence, context = await self.retriever.retrieve(query)
        return evidence, context, DecisionPoint(
            step="retrieve",
            decision="retrieved_hybrid_context",
            reason="Collected evidence from vector, graph and keyword retrieval.",
            confidence=0.8,
        )
