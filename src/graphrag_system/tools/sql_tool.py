from graphrag_system.tools.base import BaseTool


class SqlTool(BaseTool):
    name = "sql"
    description = "Run approved read-only SQL queries."

    def run(self, query: str):
        if any(token in query.lower() for token in ["delete", "drop", "truncate", "update", "insert"]):
            raise ValueError("Only read-only SQL is allowed.")
        return []
