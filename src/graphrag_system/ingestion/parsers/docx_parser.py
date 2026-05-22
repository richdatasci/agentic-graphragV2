from pathlib import Path

from graphrag_system.ingestion.models import ParsedDocument
from graphrag_system.utils.hashing import stable_hash


class DocxParser:
    def parse(self, path: str) -> ParsedDocument:
        file_path = Path(path)
        try:
            from docx import Document

            doc = Document(path)
            text = "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            text = file_path.read_text(encoding="utf-8", errors="ignore")

        return ParsedDocument(
            document_id=f"doc_{stable_hash(str(file_path))[:16]}",
            title=file_path.name,
            text=text,
            source_type="docx",
            metadata={"parser": "python-docx"},
        )
