# Data Model

## Graph Nodes

Recommended labels:

```text
Document
Chunk
Entity
Claim
Triple
Person
Organisation
System
Component
Requirement
Risk
Control
Process
Dataset
Model
Tool
Source
Conversation
AgentRun
ToolCall
Evidence
EvaluationResult
```

## Graph Relationships

Recommended relationship types:

```text
CONTAINS
MENTIONS
STATES
SUPPORTS
CONTRADICTS
DEPENDS_ON
PART_OF
IMPLEMENTS
USES
OWNS
AUTHORISED_BY
DERIVED_FROM
HAS_SOURCE
HAS_CONFIDENCE
EVALUATED_BY
```

## Relational Tables

Recommended Postgres tables:

- `documents`
- `document_versions`
- `chunks`
- `ingestion_jobs`
- `sources`
- `source_permissions`
- `agent_sessions`
- `agent_runs`
- `tool_calls`
- `evaluation_runs`
- `audit_logs`

## Triple Shape

```json
{
  "id": "triple_001",
  "subject": "GraphRAG ingestion pipeline",
  "predicate": "generates",
  "object": "entity relationship triples",
  "confidence": 0.87,
  "source_document_id": "doc_001",
  "chunk_id": "chunk_001"
}
```
