from collections import Counter


class MetricsRegistry:
    def __init__(self) -> None:
        self.counters = Counter()

    def increment(self, name: str, amount: int = 1) -> None:
        self.counters[name] += amount

    def snapshot(self) -> dict:
        return dict(self.counters)
