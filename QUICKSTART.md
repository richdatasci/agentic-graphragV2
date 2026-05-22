# Quickstart

This repo is a runnable local development version of the Agentic GraphRAG platform.

It starts:

- FastAPI API
- Celery worker
- React frontend
- Postgres
- Redis
- Neo4j Community
- Qdrant
- MinIO
- Ollama

The default setup is free and local-first. External API keys are optional and are left as `INSERT API KEY HERE`.

## 1. Prerequisites

Install:

- Docker Desktop or Docker Engine
- Docker Compose
- Make

Optional for running outside Docker:

- Python 3.11+
- Node.js 20+

## 2. Start the full local stack

```bash
cp .env.example .env
make up
```

## 3. Bootstrap local services

```bash
make bootstrap
```

This will:

- check service connectivity
- create the MinIO bucket when possible
- create the Qdrant collection when possible
- create basic Neo4j constraints when possible
- create basic Postgres tables when possible

## 4. Ingest sample data

```bash
make ingest-sample
```

## 5. Open the apps

Frontend:

```text
http://localhost:5173
```

API docs:

```text
http://localhost:8000/docs
```

Neo4j browser:

```text
http://localhost:7474
```

Qdrant dashboard:

```text
http://localhost:6333/dashboard
```

MinIO console:

```text
http://localhost:9001
```

## 6. Optional local model setup

The project defaults to Ollama.

Pull a smaller model for laptop use:

```bash
make pull-model-small
```

Or pull the better default model:

```bash
make pull-model
```

If no Ollama model is available, the API still starts and returns safe fallback responses.

## 7. Run tests

```bash
make test
```

## 8. Stop everything

```bash
make down
```

## Notes

This is a working development scaffold. The major architectural paths are present and runnable, but several production integrations are deliberately simple:

- sample ingestion is file-based
- faithfulness uses a lexical baseline evaluator
- vector search and graph search have local-safe fallbacks
- external provider keys are placeholders

The next production step is to strengthen persistence and connect real extraction outputs to Neo4j, Qdrant and Postgres.
