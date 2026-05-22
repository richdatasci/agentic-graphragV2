class ConfidenceScorer:
    def score_text_support(self, statement: str, context: str) -> float:
        statement_terms = set(statement.lower().split())
        context_terms = set(context.lower().split())
        if not statement_terms:
            return 0.0
        return len(statement_terms & context_terms) / len(statement_terms)
