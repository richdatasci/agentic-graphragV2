from graphrag_system.agents.state import DecisionPoint


class PlannerAgent:
    def plan(self, query: str) -> tuple[str, list[DecisionPoint]]:
        lowered = query.lower()
        if any(word in lowered for word in ["relationship", "depends", "graph", "connected"]):
            strategy = "hybrid"
        elif any(word in lowered for word in ["exact", "id", "part number"]):
            strategy = "keyword"
        else:
            strategy = "hybrid"

        return strategy, [
            DecisionPoint(
                step="plan",
                decision=f"use_{strategy}_retrieval",
                reason="Strategy selected from query features.",
                confidence=0.75,
            )
        ]
