import json
from pathlib import Path

from graphrag_system.extraction.entity_extractor import EntityExtractor
from graphrag_system.extraction.relationship_extractor import RelationshipExtractor
from graphrag_system.extraction.triple_extractor import TripleExtractor
from graphrag_system.ingestion.chunking.semantic_chunker import SemanticChunker
from graphrag_system.ingestion.models import ParsedDocument
from graphrag_system.llm.embedding_gateway import EmbeddingGateway
from graphrag_system.storage.vector.base import VectorRecord
from graphrag_system.storage.vector.local_store import LocalJsonVectorStore


def load_sample_docs() -> list[ParsedDocument]:
    docs = []
    for path in sorted(Path("examples/documents").glob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        docs.append(
            ParsedDocument(
                document_id=f"sample_{path.stem}",
                title=path.name,
                text=text,
                source_type="sample",
                metadata={
                    "title": path.name, "path": str(path),
                    "source_allowed_roles": ["viewer", "analyst", "admin"],
                    "document_allowed_roles": ["viewer", "analyst", "admin"],
                },
            )
        )
    return docs


def main() -> int:
    Path(".local_data").mkdir(exist_ok=True)

    chunker = SemanticChunker(max_chars=900, overlap_chars=120)
    embedder = EmbeddingGateway()
    vector_store = LocalJsonVectorStore()
    entity_extractor = EntityExtractor()
    relationship_extractor = RelationshipExtractor()
    triple_extractor = TripleExtractor()

    all_chunks = []
    all_triples = []
    vector_records = []

    for document in load_sample_docs():
        chunks = chunker.chunk(document)
        for chunk in chunks:
            all_chunks.append(chunk.model_dump())
            vector_records.append(
                VectorRecord(
                    id=chunk.id,
                    vector=embedder.embed_text(chunk.text),
                    text=chunk.text,
                    metadata={
                        **chunk.metadata,
                        "document_id": document.document_id,
                        "title": document.title,
                        "chunk_index": chunk.index,
                    },
                )
            )

        entities = entity_extractor.extract(document.text)
        relationships = relationship_extractor.extract(document.text, entities)
        triples = triple_extractor.extract(document.text, entities, relationships)

        for triple in triples:
            payload = triple.model_dump()
            payload["source_document_id"] = document.document_id
            payload["metadata"].update(document.metadata)
            payload["chunk_id"] = chunks[0].id if chunks else None
            all_triples.append(payload)

    vector_store.upsert(vector_records)
    Path(".local_data/chunks.json").write_text(json.dumps(all_chunks, indent=2), encoding="utf-8")
    Path(".local_data/triples.json").write_text(json.dumps(all_triples, indent=2), encoding="utf-8")

    print(f"Indexed documents: {len(load_sample_docs())}")
    print(f"Indexed chunks: {len(all_chunks)}")
    print(f"Indexed triples: {len(all_triples)}")
    print("Sample ingestion complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
