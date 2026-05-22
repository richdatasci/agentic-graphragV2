# Governance and Security Sample

The platform must enforce role-based access control. Users should only retrieve documents they are permitted to access.

The system must not expose hidden chain-of-thought. It should expose a structured decision trace instead.

The decision trace can show selected retrieval strategy, tools used, evidence used, graph queries, evaluator result and unsupported claims.

Prompt injection should be handled through source sanitisation, tool restrictions and governance filters.

PII should be detected and redacted before being exposed to users without permission.
