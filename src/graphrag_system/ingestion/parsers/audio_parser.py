from pathlib import Path

from graphrag_system.ingestion.models import ParsedDocument
from graphrag_system.utils.hashing import stable_hash


class AudioParser:
    def parse(self, path: str) -> ParsedDocument:
        file_path = Path(path)
        text = f"Audio transcription placeholder for {file_path.name}."
        return ParsedDocument(
            document_id=f"audio_{stable_hash(str(file_path))[:16]}",
            title=file_path.name,
            text=text,
            source_type="audio",
            metadata={"parser": "whisper_placeholder"},
        )
