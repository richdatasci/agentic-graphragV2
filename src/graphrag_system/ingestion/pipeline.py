from pathlib import Path
from typing import Any

from graphrag_system.connectors.local_files import LocalFileConnector
from graphrag_system.ingestion.chunking.semantic_chunker import SemanticChunker
from graphrag_system.ingestion.enrichment.document_classifier import DocumentClassifier
from graphrag_system.ingestion.enrichment.metadata import MetadataEnricher
from graphrag_system.ingestion.enrichment.pii_detection import PiiDetector
from graphrag_system.ingestion.models import ParsedDocument


class IngestionPipeline:
    def __init__(self) -> None:
        self.chunker = SemanticChunker()
        self.metadata = MetadataEnricher()
        self.pii = PiiDetector()
        self.classifier = DocumentClassifier()

    def ingest_source(self, source_payload: dict[str, Any]) -> dict[str, Any]:
        source_type = source_payload.get("source_type")
        source_uri = source_payload.get("source_uri")

        if source_type == "local_file" and source_uri:
            documents = LocalFileConnector(source_uri).load()
        else:
            documents = []

        parsed_docs = [
            ParsedDocument(
                document_id=doc.id,
                title=doc.title,
                text=doc.content,
                source_type=doc.source_type,
                metadata=doc.metadata,
            )
            for doc in documents
        ]

        return self._process_documents(parsed_docs)

    def ingest_uploaded_file(self, file_payload: dict[str, Any]) -> dict[str, Any]:
        text = file_payload.get("text", "")
        parsed = ParsedDocument(
            document_id=file_payload.get("document_id", "uploaded_doc"),
            title=file_payload.get("filename", "uploaded_file"),
            text=text,
            source_type="uploaded_file",
            metadata=file_payload.get("metadata", {}),
        )
        return self._process_documents([parsed])

    def reprocess_document(self, document_id: str, options: dict[str, Any]) -> dict[str, Any]:
        return {"status": "accepted", "document_id": document_id, "options": options}

    def _process_documents(self, documents: list[ParsedDocument]) -> dict[str, Any]:
        chunk_count = 0
        processed = []
        for doc in documents:
            doc = self.metadata.enrich(doc)
            doc.metadata["document_class"] = self.classifier.classify(doc.text)
            doc.metadata["pii"] = self.pii.find(doc.text)
            chunks = self.chunker.chunk(doc)
            chunk_count += len(chunks)
            processed.append({"document": doc.model_dump(), "chunks": [c.model_dump() for c in chunks]})

        return {"status": "completed", "document_count": len(documents), "chunk_count": chunk_count, "processed": processed}
