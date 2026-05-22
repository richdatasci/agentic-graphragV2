from graphrag_system.connectors.base import BaseConnector, SourceDocument


class ConfluenceConnector(BaseConnector):
    """Placeholder connector. Add Confluence API token when wiring this."""

    def __init__(self, base_url: str, api_token: str = "INSERT API KEY HERE") -> None:
        self.base_url = base_url
        self.api_token = api_token

    def load(self) -> list[SourceDocument]:
        return []
