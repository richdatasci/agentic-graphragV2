from contextlib import contextmanager
from typing import Any, Iterator

try:
    from neo4j import READ_ACCESS, GraphDatabase, Query
except Exception:
    GraphDatabase = None


class Neo4jClient:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "agentic-graphrag-password") -> None:
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(uri, auth=(user, password)) if GraphDatabase else None

    def close(self) -> None:
        if self.driver:
            self.driver.close()

    def execute_write(self, query: str, parameters: dict[str, Any]) -> list[dict[str, Any]]:
        if not self.driver:
            return []
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def execute_read(self, query: str, parameters: dict[str, Any]) -> list[dict[str, Any]]:
        if not self.driver:
            return []
        with self.driver.session(default_access_mode=READ_ACCESS) as session:
            result = session.run(Query(query, timeout=5), parameters)
            return [record.data() for record in result]
