import json
from typing import Any


def safe_json_loads(value: str, default: Any = None) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


def to_pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=str)
