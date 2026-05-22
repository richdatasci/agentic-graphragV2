class GraphAgent:
    def build_query(self, question: str) -> str:
        return "MATCH (n) RETURN n LIMIT 25"
