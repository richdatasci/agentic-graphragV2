from rapidfuzz import process


class FuzzySearcher:
    def search(self, query: str, choices: list[str], limit: int = 10) -> list[tuple[str, float]]:
        return [(match, score) for match, score, _ in process.extract(query, choices, limit=limit)]
