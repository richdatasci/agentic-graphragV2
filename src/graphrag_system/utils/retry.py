from collections.abc import Callable
from time import sleep
from typing import TypeVar

T = TypeVar("T")


def retry_sync(fn: Callable[[], T], attempts: int = 3, delay_seconds: float = 0.5) -> T:
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            return fn()
        except Exception as exc:
            last_error = exc
            sleep(delay_seconds)
    if last_error:
        raise last_error
    raise RuntimeError("Retry failed without exception.")
