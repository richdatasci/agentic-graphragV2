from contextlib import contextmanager
from time import perf_counter


@contextmanager
def trace_span(name: str):
    start = perf_counter()
    try:
        yield
    finally:
        elapsed = perf_counter() - start
        print(f"trace_span={name} elapsed_seconds={elapsed:.6f}")
