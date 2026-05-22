from typing import Iterable, TypeVar

T = TypeVar("T")


class Deduplicator:
    def by_attr(self, items: Iterable[T], attr: str) -> list[T]:
        seen = set()
        output = []
        for item in items:
            value = getattr(item, attr)
            if value in seen:
                continue
            seen.add(value)
            output.append(item)
        return output
