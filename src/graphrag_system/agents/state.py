from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field

from graphrag_system.retrieval.vector_retriever import RetrievedEvidence


class DecisionPoint(BaseModel):
    step: str
    decision: str
    reason: str
    confidence: float | None = None


class AgentRunResult(BaseModel):
    session_id: str
    final_answer: str
    run_id: str = ""
    evidence: list[RetrievedEvidence] = Field(default_factory=list)
    decision_trace: list[DecisionPoint] = Field(default_factory=list)
    faithfulness_score: float | None = None
    unsupported_claims: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


@dataclass
class AgentState:
    session_id: str
    user_query: str
    roles: list[str] = field(default_factory=lambda: ["viewer"])
    history: list[dict[str, str]] = field(default_factory=list)
    rewritten_query: str = ""
    retrieval_strategy: str = "hybrid"
    evidence: list[RetrievedEvidence] = field(default_factory=list)
    context: str = ""
    decision_trace: list[DecisionPoint] = field(default_factory=list)
    draft_answer: str = ""
    final_answer: str = ""
    evaluation: dict = field(default_factory=dict)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    backends: dict[str, str] = field(default_factory=dict)
    attempts: int = 0
