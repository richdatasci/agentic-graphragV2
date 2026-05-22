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
