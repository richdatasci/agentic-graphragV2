from graphrag_system.graph_presentation.triples_preview import TriplePreviewService
from graphrag_system.tools.base import BaseTool


class TripleSearchTool(BaseTool):
    name = "triple_search"
    description = "Fuzzy search extracted graph triples."

    def run(self, query: str, limit: int = 25):
        return TriplePreviewService().search(query, limit=limit)
