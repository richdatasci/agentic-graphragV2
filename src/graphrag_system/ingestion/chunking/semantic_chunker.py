from graphrag_system.ingestion.models import DocumentChunk, ParsedDocument
from graphrag_system.utils.hashing import stable_hash


class SemanticChunker:
    def __init__(self, max_chars: int = 1800, overlap_chars: int = 200) -> None:
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars

    def chunk(self, document: ParsedDocument) -> list[DocumentChunk]:
        text = document.text.strip()
        if not text:
            return []
        chunks: list[DocumentChunk] = []
        start = 0
        index = 0
        while start < len(text):
            end = min(len(text), start + self.max_chars)
            chunk_text = text[start:end].strip()
            chunks.append(
                DocumentChunk(
                    id=f"chunk_{stable_hash(document.document_id + str(index) + chunk_text)[:16]}",
                    document_id=document.document_id,
                    text=chunk_text,
                    index=index,
                    metadata=document.metadata,
                )
            )
            if end == len(text):
                break
            start = max(0, end - self.overlap_chars)
            index += 1
        return chunks
