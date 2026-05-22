from graphrag_system.evaluation.faithfulness import FaithfulnessEvaluator


class HallucinationChecker:
    def check(self, answer: str, contexts: list[str]) -> dict:
        result = FaithfulnessEvaluator().evaluate(answer, contexts)
        return {
            "hallucination_risk": 1 - result["faithfulness_score"],
            "unsupported_claims": [
                c["claim"] for c in result["claims"] if c["status"] == "unsupported"
            ],
        }
