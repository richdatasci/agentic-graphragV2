from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from apps.api.dependencies import AppContainer, get_app_container
from graphrag_system.agents.supervisor import SupervisorAgent
from graphrag_system.llm.model_gateway import ModelGateway
from graphrag_system.retrieval.hybrid_retriever import HybridRetriever

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    session_id: str | None = None
    include_decision_trace: bool = True
    include_graph_preview: bool = True
    history: list[ChatMessage] = Field(default_factory=list)


class EvidenceItem(BaseModel):
    source_id: str
    chunk_id: str | None = None
    title: str | None = None
    score: float | None = None
    source_type: str


class DecisionTraceItem(BaseModel):
    step: str
    decision: str
    reason: str
    confidence: float | None = None


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    evidence: list[EvidenceItem] = Field(default_factory=list)
    decision_trace: list[DecisionTraceItem] = Field(default_factory=list)
    faithfulness_score: float | None = None
    unsupported_claims: list[str] = Field(default_factory=list)


@router.post("", response_model=ChatResponse)
async def create_chat_completion(
    request: ChatRequest,
    container: AppContainer = Depends(get_app_container),
) -> ChatResponse:
    if not request.query.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query cannot be empty.")

    gateway = ModelGateway.from_settings(container.settings)
    retriever = HybridRetriever()
    supervisor = SupervisorAgent(model_gateway=gateway, retriever=retriever)

    result = await supervisor.run(
        query=request.query,
        session_id=request.session_id or "local-session",
        history=[m.model_dump() for m in request.history],
    )

    return ChatResponse(
        session_id=result.session_id,
        answer=result.final_answer,
        evidence=[EvidenceItem(**e.model_dump()) for e in result.evidence],
        decision_trace=[DecisionTraceItem(**d.model_dump()) for d in result.decision_trace],
        faithfulness_score=result.faithfulness_score,
        unsupported_claims=result.unsupported_claims,
    )


@router.get("/{session_id}/history")
async def get_chat_history(session_id: str) -> dict[str, Any]:
    return {"session_id": session_id, "messages": [], "status": "memory_store_pending"}


@router.get("/runs/{run_id}/trace")
async def get_agent_run_trace(run_id: str) -> dict[str, Any]:
    return {"run_id": run_id, "decision_trace": [], "tool_calls": [], "evidence": []}
