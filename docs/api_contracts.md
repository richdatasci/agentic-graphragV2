# API Contracts

## Chat

```text
POST /chat
GET  /chat/{session_id}/history
GET  /chat/runs/{run_id}/trace
```

## Ingestion

```text
POST /ingestion/jobs
POST /ingestion/files
GET  /ingestion/jobs/{job_id}
```

## Documents

```text
GET /documents
GET /documents/{document_id}
GET /documents/{document_id}/chunks
```

## Graph

```text
GET /graph/entities/search
GET /graph/entities/{entity_id}/neighbours
GET /graph/path
GET /graph/subgraph
GET /graph/schema
```

## Triples

```text
GET /triples/search
GET /triples/{triple_id}
```

## Evaluation

```text
POST /evaluation/faithfulness
POST /evaluation/runs
GET  /evaluation/runs/{run_id}
```

## Admin

```text
GET /admin/status
GET /admin/config
GET /admin/metrics
```

## Chat response and session

`POST /chat` accepts an optional UUIDv4 `session_id`. Omit it for a new
session and reuse the returned ID for follow-up turns. Keep session IDs
private. Responses include a `run_id`, citation-labelled evidence and
faithfulness and relevance scores when the evaluator ran. Set
`include_decision_trace` or `include_graph_preview` to false to omit those
parts of the chat response.

Send the session ID in the `X-Session-ID` header on trace requests. The trace
includes routing and backend outcomes, approved tool calls, evidence identifiers,
and evaluator results. History and trace requests use the same authentication
as chat. History and traces expire when purged from the process cache or when
the API process restarts.
