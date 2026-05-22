# Agentic GraphRAG Architecture Sample

Agentic GraphRAG combines graph retrieval, vector search, keyword search and multi-agent orchestration.

The ingestion layer parses documents, images, tables, audio transcripts and API payloads. It creates chunks, extracts entities, identifies relationships and generates graph triples.

The graph database stores entities, claims, triples and document lineage. Neo4j is the default graph database for the local development stack.

The vector database stores embeddings for document chunks, table summaries, image captions and extracted claims. Qdrant is the default vector database.

The supervisor agent routes work to planner, retriever, graph, vector, tool, synthesiser and evaluator agents.

Faithfulness evaluation checks whether generated answer claims are supported by retrieved context.
