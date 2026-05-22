from pathlib import Path

from graphrag_system.ingestion.models import ParsedDocument
from graphrag_system.utils.hashing import stable_hash


class PptxParser:
    def parse(self, path: str) -> ParsedDocument:
        file_path = Path(path)
        try:
            from pptx import Presentation

            prs = Presentation(path)
            texts = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        texts.append(shape.text)
            text = "\n".join(texts)
        except Exception:
            text = ""

        return ParsedDocument(
            document_id=f"doc_{stable_hash(str(file_path))[:16]}",
            title=file_path.name,
            text=text,
            source_type="pptx",
            metadata={"parser": "python-pptx"},
        )
