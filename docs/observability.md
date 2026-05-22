# Observability

The system should be observable across API, workers, retrieval, graph, vector and model calls.

## Metrics

- API request latency
- API error rate
- worker job duration
- ingestion throughput
- graph query latency
- vector query latency
- model latency
- token usage
- evaluation score trends
- unsupported claim count

## Traces

Trace:

- request ID
- session ID
- agent run ID
- planner decision
- retrieval calls
- tool calls
- model calls
- evaluator calls

## Logs

Use structured logs with:

- timestamp
- level
- service
- request ID
- session ID
- run ID
- event name
- metadata
