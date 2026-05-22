# Evaluation

Evaluation is central to production GraphRAG.

## Primary Metrics

- Faithfulness
- Context precision
- Context recall
- Answer relevance
- Unsupported claim count
- Tool-call success rate
- Retrieval latency
- Answer latency

## Faithfulness Flow

```text
Generated answer
→ split into claims
→ check each claim against retrieved context
→ classify supported, partially supported or unsupported
→ calculate score
→ allow, caution, regenerate or refuse
```

## Suggested Thresholds

| Score | Action |
|---|---|
| 0.90 to 1.00 | Allow |
| 0.75 to 0.89 | Allow with caution |
| 0.50 to 0.74 | Regenerate |
| Below 0.50 | Refuse or request more evidence |
