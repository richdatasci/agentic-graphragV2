from pydantic import BaseModel


class SecurityPolicy(BaseModel):
    allow_external_tools: bool = False
    redact_pii: bool = True
    expose_decision_trace: bool = True
    expose_chain_of_thought: bool = False
    max_tool_calls: int = 8
