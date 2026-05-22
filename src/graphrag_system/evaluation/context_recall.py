class ContextRecallEvaluator:
    def evaluate(self, relevant_retrieved: int, total_relevant: int) -> float:
        if total_relevant == 0:
            return 0.0
        return relevant_retrieved / total_relevant
