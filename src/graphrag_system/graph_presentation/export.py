import json


class GraphExporter:
    def to_json(self, subgraph: dict) -> str:
        return json.dumps(subgraph, indent=2, ensure_ascii=False)

    def to_cytoscape(self, subgraph: dict) -> dict:
        elements = []
        for node in subgraph.get("nodes", []):
            elements.append({"data": node})
        for edge in subgraph.get("edges", []):
            elements.append({"data": edge})
        return {"elements": elements}
