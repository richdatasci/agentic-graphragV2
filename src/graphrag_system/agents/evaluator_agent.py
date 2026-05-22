from graphrag_system.evaluation.faithfulness import FaithfulnessEvaluator


class EvaluatorAgent:
    def __init__(self) -> None:
        self.faithfulness = FaithfulnessEvaluator()

    def evaluate(self, answer: str, contexts: list[str]) -> dict:
        return self.faithfulness.evaluate(answer, contexts)
