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
