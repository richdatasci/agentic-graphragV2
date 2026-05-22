# Runbook

## API Is Down

1. Check pod or container status.
2. Check `/health`.
3. Check logs.
4. Check database connectivity.
5. Check environment variables and secrets.

## Worker Jobs Are Stuck

1. Check Redis connectivity.
2. Check Celery worker logs.
3. Check queue depth.
4. Restart worker deployment if needed.
5. Inspect failed task payloads.

## Retrieval Quality Is Poor

1. Inspect retrieved chunks.
2. Check vector index freshness.
3. Check graph extraction quality.
4. Check reranker behaviour.
5. Run evaluation notebook.

## Faithfulness Scores Drop

1. Inspect unsupported claims.
2. Check retrieved evidence.
3. Check prompt changes.
4. Check model changes.
5. Run regression evaluation.
