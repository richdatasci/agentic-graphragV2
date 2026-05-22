from typing import Any, Literal

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
    evidence: list[RetrievedEvidence] = Field(default_factory=list)
    decision_trace: list[DecisionPoint] = Field(default_factory=list)
    faithfulness_score: float | None = None
    unsupported_claims: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentState(BaseModel):
    session_id: str
    user_query: str
    rewritten_query: str | None = None
    intent: str | None = None
    retrieval_strategy: Literal["vector", "graph", "keyword", "hybrid", "tool_augmented"] = "hybrid"
    evidence: list[RetrievedEvidence] = Field(default_factory=list)
    decision_trace: list[DecisionPoint] = Field(default_factory=list)
    draft_answer: str | None = None
    final_answer: str | None = None
    faithfulness_score: float | None = None
    unsupported_claims: list[str] = Field(default_factory=list)
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
