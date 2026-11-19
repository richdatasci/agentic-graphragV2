# Agents

The multi-agent system should be orchestrated by a supervisor.

## Agents

| Agent | Responsibility |
|---|---|
| Supervisor Agent | Owns the run and routes between agents |
| Planner Agent | Breaks the task into steps |
| Retriever Agent | Selects graph, vector, keyword or hybrid retrieval |
| Graph Agent | Builds graph queries or calls graph tools |
| Vector Agent | Performs semantic search and query rewriting |
| Tool Agent | Calls approved tools |
| Synthesiser Agent | Creates the final answer |
| Evaluator Agent | Runs faithfulness and quality checks |
| Memory Agent | Manages session context |
| Governance Agent | Applies policy and access controls |

## Decision Trace

Expose:

- selected strategy
- tools used
- evidence used
- confidence scores
- evaluator results
- unsupported claims

Do not expose hidden chain-of-thought.

## Runtime

`POST /chat` runs the agents through LangGraph. The planner selects keyword,
graph, vector or hybrid retrieval from question cues. An empty specialised route
broadens to the remaining backends. Hybrid retrieval can continue when one backend
fails. Graph retrieval expands around matching edges. The supervisor filters
evidence by source and document permissions, removes common prompt-control
directives, redacts email addresses, and packs and numbers eligible evidence.

Answers cite the packed sources. The evaluator checks citation references,
lexical support, numbers and negation and records answer relevance. A draft that
fails verification receives one retry. Empty indexes, unavailable models and
unverified drafts produce an explicit abstention. The evaluator is a lexical
baseline and can miss semantic contradictions.

The default backend uses the local indexes from `make ingest-sample`.
`CHAT_GRAPH_BACKEND=neo4j` enables the parameterised Triple search.
Triple nodes need `subject`, `predicate`, `object` and `source_document_id`.
`CHAT_VECTOR_BACKEND=qdrant` enables the configured vector collection.
Its payloads need `text` and `document_id`, and the collection must use the
configured embedding model and dimensions. Indexed records can carry
`source_allowed_roles` and `document_allowed_roles`. Both policies must allow
the request. Use read-only provider credentials for the remote search backends.

To enable external tool evidence, register a server-owned `BaseTool` and name
it as `search_tool` when constructing the supervisor. The selected adapter
receives bounded `query` and `top_k` arguments and returns a list of
`RetrievedEvidence` records. The same evidence policy applies to those records.
Configure fixed endpoints or parameterised, read-only queries inside the
adapter. Tool selection stays in server configuration.

Session memory and traces are bounded to one API process. Local chat without
a key uses viewer access. The bundled examples are readable by viewers, including
indexes created before explicit sample permissions were added. Set
`CHAT_API_KEY` and send it as an Authorization bearer token for authenticated
admin access. Non-local chat requires this key unless the application supplies
its own authentication dependency. This is a single-key deployment option.
