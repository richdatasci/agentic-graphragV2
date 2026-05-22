from graphrag_system.ingestion.enrichment.pii_detection import PiiDetector


class Redactor:
    def __init__(self) -> None:
        self.pii = PiiDetector()

    def redact(self, text: str) -> str:
        return self.pii.redact(text)
