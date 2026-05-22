from graphrag_system.graph_presentation.subgraph_builder import SubgraphBuilder
from graphrag_system.tools.base import BaseTool


class GraphVisualisationTool(BaseTool):
    name = "graph_visualisation"
    description = "Build a graph visualisation payload."

    def run(self, entity_id: str, depth: int = 2):
        return SubgraphBuilder().placeholder_neighbourhood(entity_id, depth)
