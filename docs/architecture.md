# Architecture

The Agentic GraphRAG platform is split into two main planes.

## Offline Ingestion Plane

The ingestion plane handles source loading, parsing, OCR, image understanding, chunking, metadata enrichment, entity extraction, relationship extraction, claim extraction, triple generation, embedding generation and indexing.

Flow:

```text
Data source
→ connector
→ parser
→ chunker
→ enrichment
→ extraction
→ graph write
→ vector write
→ metadata write
```

## Online Query Plane

The query plane handles user questions, intent classification, planning, graph retrieval, vector retrieval, keyword retrieval, tool use, answer synthesis, faithfulness evaluation and decision trace generation.

Flow:

```text
User question
→ supervisor agent
→ planner
→ retriever
→ graph/vector/keyword/tools
→ context packer
→ answer synthesiser
→ evaluator
→ response with evidence and decision trace
```

## Key Components

- FastAPI API layer
- Celery worker layer
- Neo4j graph database
- Qdrant vector database
- Postgres metadata database
- MinIO object storage
- Redis queue and cache
- Ollama local model gateway
- React frontend
