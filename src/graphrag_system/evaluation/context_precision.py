class ContextPrecisionEvaluator:
    def evaluate(self, relevant_contexts: int, retrieved_contexts: int) -> float:
        if retrieved_contexts == 0:
            return 0.0
        return relevant_contexts / retrieved_contexts
