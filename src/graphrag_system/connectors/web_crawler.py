import httpx
from bs4 import BeautifulSoup

from graphrag_system.connectors.base import BaseConnector, SourceDocument
from graphrag_system.utils.hashing import stable_hash


class WebCrawlerConnector(BaseConnector):
    def __init__(self, url: str) -> None:
        self.url = url

    def load(self) -> list[SourceDocument]:
        response = httpx.get(self.url, timeout=30.0)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup(["script", "style", "noscript"]):
            element.extract()
        text = soup.get_text("\n")
        return [
            SourceDocument(
                id=f"web_{stable_hash(self.url)[:12]}",
                title=soup.title.string if soup.title else self.url,
                content="\n".join(line.strip() for line in text.splitlines() if line.strip()),
                source_type="web",
                uri=self.url,
            )
        ]
