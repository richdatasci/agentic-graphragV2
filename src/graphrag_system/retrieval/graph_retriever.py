import json
import re
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path

from graphrag_system.retrieval.vector_retriever import RetrievedEvidence
from graphrag_system.storage.graph.neo4j_client import Neo4jClient

SEARCH_TRIPLES = """
MATCH (t:Triple)
WHERE t.source_document_id IS NOT NULL
  AND any(term IN $terms WHERE
    toLower(coalesce(t.subject, '')) CONTAINS term OR
    toLower(coalesce(t.predicate, '')) CONTAINS term OR
    toLower(coalesce(t.object, '')) CONTAINS term)
RETURN t.subject AS subject, t.predicate AS predicate, t.object AS object,
       t.source_document_id AS source_document_id, t.chunk_id AS chunk_id,
       t.source_allowed_roles AS source_allowed_roles,
       t.document_allowed_roles AS document_allowed_roles
ORDER BY t.confidence DESC, t.id
LIMIT $limit
"""

EvidenceFilter = Callable[[list[RetrievedEvidence]], list[RetrievedEvidence]]
QUERY_STOP_WORDS = {
    "a", "an", "and", "are", "between", "connected", "does", "find", "how", "in", "is",
    "neighbors", "neighbours", "of", "path", "show", "the", "to", "what", "which",
}


class GraphRetriever:
    def __init__(self, client: Neo4jClient | None = None) -> None:
        self.client = client

    def retrieve(
        self, query: str, top_k: int = 8, *, evidence_filter: EvidenceFilter | None = None,
    ) -> list[RetrievedEvidence]:
        query_terms = set(re.findall(r"\w+", query.casefold())) - QUERY_STOP_WORDS
        if not query_terms:
            return []
        if self.client:
            triples = self.client.execute_read(
                SEARCH_TRIPLES, {"terms": sorted(query_terms)[:40], "limit": top_k * 4},
            )
        else:
            path = Path(".local_data/triples.json")
            if not path.exists():
                return []
            triples = json.loads(path.read_text(encoding="utf-8"))
        edges = [
            RetrievedEvidence(
                source_id=triple.get("source_document_id") or "local_graph",
                chunk_id=triple.get("chunk_id"),
                title="Local graph triple",
                text=f"{triple['subject']} {triple['predicate']} {triple['object']}",
                source_type="graph",
                metadata={**triple.get("metadata", {}), **{
                    key: value for key, value in triple.items() if value is not None
                }},
            )
            for triple in triples
        ]
        if evidence_filter:
            edges = evidence_filter(edges)

        by_node = defaultdict(list)
        endpoints = []
        scores = {}
        for index, item in enumerate(edges):
            subject = item.metadata["subject"].casefold()
            target = item.metadata["object"].casefold()
            endpoints.append((subject, target))
            by_node[subject].append(index)
            by_node[target].append(index)
            terms = set(re.findall(r"\w+", item.text.casefold()))
            overlap = len(query_terms & terms)
            if overlap:
                scores[index] = overlap / len(query_terms)

        # Expand from the strongest matching edges by one additional hop.
        seeds = sorted(scores, key=scores.__getitem__, reverse=True)[:top_k]
        for seed in seeds:
            for node in endpoints[seed]:
                for neighbor in by_node[node]:
                    scores.setdefault(neighbor, scores[seed] * 0.5)
        ranked = sorted(scores, key=scores.__getitem__, reverse=True)[:top_k]
        return [edges[index].model_copy(update={"score": scores[index]}) for index in ranked]
