from graphrag_system.ingestion.models import DocumentChunk, ParsedDocument
from graphrag_system.utils.hashing import stable_hash


class TableChunker:
    def chunk_tables(self, document: ParsedDocument, tables: list[str]) -> list[DocumentChunk]:
        return [
            DocumentChunk(
                id=f"table_chunk_{stable_hash(document.document_id + str(i) + table)[:16]}",
                document_id=document.document_id,
                text=table,
                index=i,
                metadata={**document.metadata, "content_type": "table"},
            )
            for i, table in enumerate(tables)
        ]
