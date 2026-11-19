import re
import unicodedata

from graphrag_system.retrieval.vector_retriever import RetrievedEvidence, VectorRetriever


class VectorAgent:
    def __init__(self, retriever: VectorRetriever | None = None) -> None:
        self.retriever = retriever or VectorRetriever()

    def rewrite_query(self, query: str) -> str:
        return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", query)).strip()

    def retrieve(self, query: str, top_k: int = 8) -> list[RetrievedEvidence]:
        return self.retriever.retrieve(self.rewrite_query(query), top_k=top_k)
