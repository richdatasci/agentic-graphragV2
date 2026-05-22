# graphrag_system source package

This scaffold contains the core Python package layout for the Agentic GraphRAG platform.

The package is intentionally split by architectural concern:

- `config`: settings, logging and security configuration
- `connectors`: external source connectors
- `ingestion`: multimodal parsing, chunking and enrichment
- `extraction`: entity, relationship, claim and triple extraction
- `storage`: graph, vector, object and relational storage adapters
- `retrieval`: hybrid retrieval, reranking, context packing and citations
- `agents`: supervisor, planner, retriever and evaluator agent logic
- `tools`: tool interfaces used by agents
- `llm`: model gateway, providers and prompt assets
- `evaluation`: faithfulness and RAG quality evaluation
- `graph_presentation`: triple preview, subgraph export and graph visualisation helpers
- `memory`: conversation and long-term memory services
- `governance`: RBAC, audit, redaction and safety controls
- `observability`: tracing, metrics, logging and cost tracking
- `utils`: shared helpers

Implementation files will be added folder by folder.
