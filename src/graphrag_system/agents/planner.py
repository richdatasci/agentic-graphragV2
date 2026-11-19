import re

from graphrag_system.agents.state import DecisionPoint


class PlannerAgent:
    def plan(self, query: str) -> tuple[str, list[DecisionPoint]]:
        strategy = "hybrid"
        routes = (
            ("keyword", r"\b(exact|id|part number|identifier|verbatim)\b"),
            ("graph", r"\b(path between|how (?:is|are) .+ connected|neighbors|neighbours)\b"),
            ("vector", r"\b(semantic(?:ally)?|similar to|paraphrase)\b"),
        )
        for route, pattern in routes:
            if re.search(pattern, query, re.IGNORECASE):
                strategy = route
                break

        return strategy, [
            DecisionPoint(
                step="plan",
                decision=f"use_{strategy}_retrieval",
                reason="Selected retrieval from question cues. Retrieve, pack, answer and verify.",
            )
        ]
