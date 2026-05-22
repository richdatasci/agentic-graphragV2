from graphrag_system.storage.graph.cypher_templates import UPSERT_ENTITY, UPSERT_TRIPLE
from graphrag_system.storage.graph.neo4j_client import Neo4jClient


class GraphWriter:
    def __init__(self, client: Neo4jClient | None = None) -> None:
        self.client = client or Neo4jClient()

    def upsert_entity(self, entity: dict) -> None:
        self.client.execute_write(UPSERT_ENTITY, entity)

    def upsert_triple(self, triple: dict) -> None:
        self.client.execute_write(UPSERT_TRIPLE, triple)
