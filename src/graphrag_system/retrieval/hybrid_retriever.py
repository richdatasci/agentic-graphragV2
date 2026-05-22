from graphrag_system.retrieval.context_packer import ContextPacker
from graphrag_system.retrieval.graph_retriever import GraphRetriever
from graphrag_system.retrieval.keyword_retriever import KeywordRetriever
from graphrag_system.retrieval.reranker import Reranker
from graphrag_system.retrieval.vector_retriever import RetrievedEvidence, VectorRetriever


class HybridRetriever:
    def __init__(self) -> None:
        self.vector = VectorRetriever()
        self.graph = GraphRetriever()
        self.keyword = KeywordRetriever()
        self.reranker = Reranker()
        self.packer = ContextPacker()

    async def retrieve(self, query: str, top_k: int = 8) -> tuple[list[RetrievedEvidence], str]:
        evidence = []
        evidence.extend(self.vector.retrieve(query, top_k=top_k))
        evidence.extend(self.graph.retrieve(query, top_k=top_k))
        evidence.extend(self.keyword.retrieve(query, top_k=top_k))
        ranked = self.reranker.rerank(query, evidence)[:top_k]
        context = self.packer.pack(ranked)
        return ranked, context
