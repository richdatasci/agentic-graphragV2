import asyncio
import logging
import math
from collections.abc import Callable

from graphrag_system.retrieval.context_packer import ContextPacker
from graphrag_system.retrieval.graph_retriever import GraphRetriever
from graphrag_system.retrieval.keyword_retriever import KeywordRetriever
from graphrag_system.retrieval.reranker import Reranker
from graphrag_system.retrieval.vector_retriever import RetrievedEvidence, VectorRetriever

logger = logging.getLogger(__name__)
Search = Callable[..., list[RetrievedEvidence]]


class HybridRetriever:
    def __init__(
        self, *, vector: VectorRetriever | None = None, graph: GraphRetriever | None = None,
    ) -> None:
        self.vector = vector or VectorRetriever()
        self.graph = graph or GraphRetriever()
        self.keyword = KeywordRetriever()
        self.reranker = Reranker()
        self.packer = ContextPacker()

    async def search(
        self, query: str, routes: dict[str, Search], top_k: int,
    ) -> tuple[list[RetrievedEvidence], dict[str, str]]:
        async def run(name: str, search: Search) -> tuple[str, list[RetrievedEvidence], str]:
            try:
                items = await asyncio.wait_for(
                    asyncio.to_thread(search, query, top_k=top_k), timeout=10,
                )
                return name, items, "ok"
            except Exception as error:  # noqa: BLE001
                logger.warning("retrieval_failed backend=%s error_type=%s", name, type(error).__name__)
                return name, [], "timeout" if isinstance(error, TimeoutError) else "failed"

        results = await asyncio.gather(*(run(name, search) for name, search in routes.items()))
        return (
            [item for _, items, _ in results for item in items],
            {name: status for name, _, status in results},
        )

    def rank(self, query: str, evidence: list[RetrievedEvidence], top_k: int) -> list[RetrievedEvidence]:
        finite = [item for item in evidence if item.score is None or math.isfinite(item.score)]
        return self.reranker.rerank(query, finite)[:top_k]

    async def retrieve(self, query: str, top_k: int = 8) -> tuple[list[RetrievedEvidence], str]:
        evidence, _ = await self.search(query, {
            "vector": self.vector.retrieve,
            "graph": self.graph.retrieve,
            "keyword": self.keyword.retrieve,
        }, top_k)
        return self.packer.pack_evidence(self.rank(query, evidence, top_k))
