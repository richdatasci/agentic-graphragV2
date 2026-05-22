from sqlalchemy import create_engine, text

from graphrag_system.connectors.base import BaseConnector, SourceDocument
from graphrag_system.utils.hashing import stable_hash


class SqlConnector(BaseConnector):
    def __init__(self, dsn: str, query: str) -> None:
        self.dsn = dsn
        self.query = query

    def load(self) -> list[SourceDocument]:
        engine = create_engine(self.dsn)
        with engine.connect() as conn:
            rows = conn.execute(text(self.query)).mappings().all()
        content = "\n".join(str(dict(row)) for row in rows)
        return [
            SourceDocument(
                id=f"sql_{stable_hash(self.query)[:12]}",
                title="SQL query result",
                content=content,
                source_type="sql",
                metadata={"row_count": len(rows)},
            )
        ]
