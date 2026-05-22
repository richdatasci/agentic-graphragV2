from pathlib import Path

from graphrag_system.ingestion.models import ParsedDocument
from graphrag_system.utils.hashing import stable_hash


class ImageParser:
    def parse(self, path: str) -> ParsedDocument:
        file_path = Path(path)
        text = ""
        try:
            import pytesseract
            from PIL import Image

            text = pytesseract.image_to_string(Image.open(path))
        except Exception:
            text = f"Image file: {file_path.name}. OCR not available."

        return ParsedDocument(
            document_id=f"img_{stable_hash(str(file_path))[:16]}",
            title=file_path.name,
            text=text,
            source_type="image",
            metadata={"parser": "pytesseract"},
        )
