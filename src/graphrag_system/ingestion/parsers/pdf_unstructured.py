from pathlib import Path

from graphrag_system.ingestion.models import ParsedDocument
from graphrag_system.utils.hashing import stable_hash


class UnstructuredPdfParser:
    def parse(self, path: str) -> ParsedDocument:
        file_path = Path(path)
        try:
            from unstructured.partition.pdf import partition_pdf

            elements = partition_pdf(filename=path)
            text = "\n".join(str(element) for element in elements)
        except Exception:
            text = file_path.read_text(encoding="utf-8", errors="ignore")

        return ParsedDocument(
            document_id=f"doc_{stable_hash(str(file_path))[:16]}",
            title=file_path.name,
            text=text,
            source_type="pdf",
            metadata={"parser": "unstructured"},
        )
