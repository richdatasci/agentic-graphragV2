from typing import Any

import httpx

from graphrag_system.connectors.base import BaseConnector, SourceDocument
from graphrag_system.utils.hashing import stable_hash


class RestApiConnector(BaseConnector):
    def __init__(self, url: str, headers: dict[str, str] | None = None) -> None:
        self.url = url
        self.headers = headers or {}

    def load(self) -> list[SourceDocument]:
        response = httpx.get(self.url, headers=self.headers, timeout=30.0)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        text = response.text
        return [
            SourceDocument(
                id=f"api_{stable_hash(self.url)[:12]}",
                title=self.url,
                content=text,
                source_type="rest_api",
                uri=self.url,
                metadata={"content_type": content_type},
            )
        ]
