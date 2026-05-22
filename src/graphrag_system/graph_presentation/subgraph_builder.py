class SubgraphBuilder:
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
