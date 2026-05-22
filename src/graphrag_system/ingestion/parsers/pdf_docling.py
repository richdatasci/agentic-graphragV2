from pathlib import Path

from graphrag_system.ingestion.models import ParsedDocument
from graphrag_system.utils.hashing import stable_hash


class DoclingPdfParser:
    """Docling parser wrapper. Falls back to plain bytes text extraction placeholder."""

    def parse(self, path: str) -> ParsedDocument:
        file_path = Path(path)
        try:
            from docling.document_converter import DocumentConverter

            converter = DocumentConverter()
            result = converter.convert(path)
            text = result.document.export_to_markdown()
        except Exception:
            text = file_path.read_text(encoding="utf-8", errors="ignore")

        return ParsedDocument(
            document_id=f"doc_{stable_hash(str(file_path))[:16]}",
            title=file_path.name,
            text=text,
            source_type="pdf",
            metadata={"parser": "docling"},
        )
