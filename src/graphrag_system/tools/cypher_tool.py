from graphrag_system.storage.graph.neo4j_client import Neo4jClient
from graphrag_system.tools.base import BaseTool


class CypherTool(BaseTool):
    name = "cypher"
    description = "Run approved read-only Cypher queries."

    def __init__(self, client: Neo4jClient | None = None) -> None:
        self.client = client or Neo4jClient()

    def run(self, query: str, parameters: dict | None = None):
        if any(token in query.lower() for token in ["delete", "detach", "remove", "set ", "create ", "merge "]):
            raise ValueError("Only read-only Cypher is allowed through this tool.")
        return self.client.execute_read(query, parameters or {})
