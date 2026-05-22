from graphrag_system.connectors.base import BaseConnector, SourceDocument


class GoogleDriveConnector(BaseConnector):
    """Placeholder connector. Add Google OAuth credentials when wiring this."""

    def __init__(self, credentials_json: str = "INSERT API KEY HERE") -> None:
        self.credentials_json = credentials_json

    def load(self) -> list[SourceDocument]:
        return []
