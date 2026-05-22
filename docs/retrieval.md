# Retrieval

The platform uses hybrid retrieval.

## Retrieval Modes

| Mode | Purpose |
|---|---|
| Vector search | Semantic similarity |
| Graph traversal | Entity relationships and multi-hop reasoning |
| Keyword search | Exact terms and IDs |
| Cypher query | Structured graph questions |
| Reranking | Improve context quality |
| Context packing | Prepare final prompt context |

## Retrieval Flow

```text
Query
→ rewrite
→ classify intent
→ select strategy
→ retrieve graph evidence
→ retrieve vector evidence
→ retrieve keyword evidence
→ rerank
→ pack context
→ generate citations
```

## Quality Checks

Track:

- top-k relevance
- context precision
- context recall
- missing evidence
- stale evidence
- duplicate chunks
- source diversity
