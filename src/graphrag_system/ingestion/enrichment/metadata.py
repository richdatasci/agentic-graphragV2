from graphrag_system.ingestion.models import ParsedDocument


class MetadataEnricher:
    def enrich(self, document: ParsedDocument) -> ParsedDocument:
        document.metadata.setdefault("character_count", len(document.text))
        document.metadata.setdefault("word_count", len(document.text.split()))
        return document
