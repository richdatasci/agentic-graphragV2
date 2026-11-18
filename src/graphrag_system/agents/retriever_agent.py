from functools import partial

from graphrag_system.agents.graph_agent import GraphAgent
from graphrag_system.agents.state import DecisionPoint
from graphrag_system.agents.vector_agent import VectorAgent
from graphrag_system.retrieval.graph_retriever import EvidenceFilter
from graphrag_system.retrieval.hybrid_retriever import HybridRetriever
from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class RetrieverAgent:
    def __init__(self, retriever: HybridRetriever | None = None) -> None:
        self.retriever = retriever or HybridRetriever()
        self.vector = VectorAgent(self.retriever.vector)
        self.graph = GraphAgent(self.retriever.graph)

    def routes(self, evidence_filter: EvidenceFilter | None = None):
        return {
            "vector": self.vector.retrieve,
            "graph": partial(self.graph.retrieve, evidence_filter=evidence_filter),
            "keyword": self.retriever.keyword.retrieve,
        }

    async def search(
        self, query: str, strategy: str, top_k: int = 8,
        *, evidence_filter: EvidenceFilter | None = None,
    ) -> tuple[list[RetrievedEvidence], dict[str, str]]:
        routes = self.routes(evidence_filter)
        if strategy not in {"hybrid", "tool_augmented"}:
            routes = {strategy: routes[strategy]}
        return await self.retriever.search(query, routes, top_k)

    async def retrieve(self, query: str) -> tuple[list[RetrievedEvidence], str, DecisionPoint]:
        evidence, context = await self.retriever.retrieve(query)
        return evidence, context, DecisionPoint(
            step="retrieve",
            decision="retrieved_hybrid_context",
            reason="Ran vector, graph and keyword retrieval.",
        )
