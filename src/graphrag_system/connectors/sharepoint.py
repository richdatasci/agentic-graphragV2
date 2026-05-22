from graphrag_system.connectors.base import BaseConnector, SourceDocument


class SharePointConnector(BaseConnector):
    """Placeholder connector. Add Microsoft Graph credentials when wiring this."""

    def __init__(self, site_url: str, access_token: str = "INSERT API KEY HERE") -> None:
        self.site_url = site_url
        self.access_token = access_token

    def load(self) -> list[SourceDocument]:
        return []
