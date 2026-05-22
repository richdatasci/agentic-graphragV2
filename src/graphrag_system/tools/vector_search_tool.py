from graphrag_system.tools.base import BaseTool


class VectorSearchTool(BaseTool):
    name = "vector_search"
    description = "Search vector store for semantically similar chunks."

    def run(self, query: str, top_k: int = 8):
        return {"query": query, "top_k": top_k, "results": []}
