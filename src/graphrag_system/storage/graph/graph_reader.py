from graphrag_system.storage.graph.neo4j_client import Neo4jClient


class GraphReader:
    def __init__(self, client: Neo4jClient | None = None) -> None:
        self.client = client or Neo4jClient()

    def search_entities(self, query: str, limit: int = 25) -> list[dict]:
        cypher = """
        MATCH (e:Entity)
        WHERE toLower(e.name) CONTAINS toLower($query)
        RETURN e.id AS id, e.name AS name, labels(e) AS labels
        LIMIT $limit
        """
        return self.client.execute_read(cypher, {"query": query, "limit": limit})

    def neighbours(self, entity_id: str, depth: int = 1) -> list[dict]:
        cypher = """
        MATCH (e {id: $entity_id})-[r]-(n)
        RETURN e, r, n
        LIMIT 100
        """
        return self.client.execute_read(cypher, {"entity_id": entity_id, "depth": depth})
