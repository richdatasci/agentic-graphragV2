from pydantic import BaseModel, Field


class ToolCallTrace(BaseModel):
    tool: str
    reason: str
    inputs: dict = Field(default_factory=dict)
    outputs_summary: str | None = None


class AgentTrace(BaseModel):
    run_id: str
    decisions: list[dict] = Field(default_factory=list)
    tool_calls: list[ToolCallTrace] = Field(default_factory=list)
