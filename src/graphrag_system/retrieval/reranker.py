from collections import defaultdict

from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class Reranker:
    def rerank(self, query: str, evidence: list[RetrievedEvidence]) -> list[RetrievedEvidence]:
        """Fuse ranked routes without comparing cosine and lexical scores directly."""
        by_route = defaultdict(list)
        for item in evidence:
            by_route[item.source_type].append(item)

        scores = defaultdict(float)
        representatives = {}
        for items in by_route.values():
            ranked = sorted(items, key=lambda item: item.score or 0.0, reverse=True)
            seen = set()
            for index, item in enumerate(ranked, start=1):
                key = (item.source_id, item.chunk_id, " ".join(item.text.casefold().split()))
                if key in seen:
                    continue
                seen.add(key)
                scores[key] += 1 / (60 + index)
                representatives.setdefault(key, item)

        return [representatives[key] for key in sorted(scores, key=scores.__getitem__, reverse=True)]
