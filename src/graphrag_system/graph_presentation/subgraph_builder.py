from graphrag_system.retrieval.vector_retriever import RetrievedEvidence
from graphrag_system.utils.hashing import stable_hash


class SubgraphBuilder:
    def from_evidence(self, evidence: list[RetrievedEvidence]) -> dict | None:
        nodes = {}
        edges = {}
        for index, item in enumerate(evidence, start=1):
            if item.source_type != "graph":
                continue
            subject = item.metadata.get("subject")
            predicate = item.metadata.get("predicate")
            target = item.metadata.get("object")
            if not all((subject, predicate, target)):
                continue
            source_id, target_id = stable_hash(subject), stable_hash(target)
            nodes[source_id] = {"id": source_id, "label": subject, "type": "Entity"}
            nodes[target_id] = {"id": target_id, "label": target, "type": "Entity"}
            edge_id = stable_hash(f"{source_id}:{predicate}:{target_id}")
            edge = edges.setdefault(edge_id, {
                "id": edge_id, "source": source_id, "target": target_id,
                "type": predicate, "citations": [],
            })
            edge["citations"].append(f"Source {index}")
        return {"nodes": list(nodes.values()), "edges": list(edges.values())} if edges else None

    def placeholder_neighbourhood(self, entity_id: str, depth: int = 1) -> dict:
        return {
            "nodes": [
                {"id": entity_id, "label": entity_id, "type": "Entity", "properties": {"depth": 0}},
                {"id": f"{entity_id}_doc", "label": "Source Document", "type": "Document", "properties": {"depth": depth}},
                {"id": f"{entity_id}_claim", "label": "Supported Claim", "type": "Claim", "properties": {"depth": depth}},
            ],
            "edges": [
                {"id": f"{entity_id}_edge_1", "source": entity_id, "target": f"{entity_id}_doc", "type": "MENTIONED_IN", "properties": {}},
                {"id": f"{entity_id}_edge_2", "source": f"{entity_id}_claim", "target": entity_id, "type": "MENTIONS", "properties": {}},
            ],
        }

    def placeholder_path(self, source: str, target: str) -> dict:
        middle = f"path_{source}_{target}"
        return {
            "nodes": [
                {"id": source, "label": source, "type": "Entity", "properties": {}},
                {"id": middle, "label": "Intermediate", "type": "Entity", "properties": {}},
                {"id": target, "label": target, "type": "Entity", "properties": {}},
            ],
            "edges": [
                {"id": f"{source}_{middle}", "source": source, "target": middle, "type": "RELATED_TO", "properties": {}},
                {"id": f"{middle}_{target}", "source": middle, "target": target, "type": "RELATED_TO", "properties": {}},
            ],
        }
