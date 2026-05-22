class TokenBudget:
    def __init__(self, max_context_chars: int = 12000) -> None:
        self.max_context_chars = max_context_chars

    def trim(self, text: str) -> str:
        return text[: self.max_context_chars]
