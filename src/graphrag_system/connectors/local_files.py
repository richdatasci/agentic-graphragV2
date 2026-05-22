from pathlib import Path

from graphrag_system.connectors.base import BaseConnector, SourceDocument
from graphrag_system.utils.hashing import stable_hash


class LocalFileConnector(BaseConnector):
    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def load(self) -> list[SourceDocument]:
        files = [self.path] if self.path.is_file() else list(self.path.rglob("*"))
        documents: list[SourceDocument] = []
        for file in files:
            if not file.is_file():
                continue
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                content = ""
            documents.append(
                SourceDocument(
                    id=f"doc_{stable_hash(str(file))[:12]}",
                    title=file.name,
                    content=content,
                    source_type="local_file",
                    uri=str(file),
                    metadata={"suffix": file.suffix},
                )
            )
        return documents
