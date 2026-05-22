# Security

## Controls

- Authentication
- Role-based access control
- Source-level permissions
- Document-level permissions
- PII detection
- Redaction
- Audit logging
- Prompt injection filtering
- Approved tool registry
- Rate limiting
- Secrets management

## Chain-of-Thought Policy

The system must not expose hidden chain-of-thought.

Expose a structured decision trace instead:

- route selected
- retrieval strategy
- tools used
- evidence used
- evaluator score
- unsupported claims
