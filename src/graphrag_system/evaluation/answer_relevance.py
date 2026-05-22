class AnswerRelevanceEvaluator:
    def evaluate(self, query: str, answer: str) -> float:
        query_terms = set(query.lower().split())
        answer_terms = set(answer.lower().split())
        if not query_terms:
            return 0.0
        return len(query_terms & answer_terms) / len(query_terms)
