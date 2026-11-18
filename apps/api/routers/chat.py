from collections import OrderedDict
from hmac import compare_digest
from threading import Lock
from typing import Annotated, Any, Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import UUID4, BaseModel, Field

from apps.api.dependencies import AppContainer, get_app_container
from graphrag_system.agents.state import DecisionPoint
from graphrag_system.agents.supervisor import SupervisorAgent
from graphrag_system.graph_presentation.subgraph_builder import SubgraphBuilder

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str = Field(max_length=4000)


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)
    session_id: UUID4 | None = None
    include_decision_trace: bool = True
    include_graph_preview: bool = True
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class EvidenceItem(BaseModel):
    source_id: str
    chunk_id: str | None = None
    title: str | None = None
    score: float | None = None
    source_type: str
    citation: str


class RunTrace(BaseModel):
    run_id: str
    retrieval_strategy: str
    intent: str
    retrieval_backends: dict[str, str] = Field(default_factory=dict)
    decision_trace: list[DecisionPoint] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    faithfulness_score: float | None = None
    answer_relevance: float | None = None
    unsupported_claims: list[str] = Field(default_factory=list)


class ChatResponse(BaseModel):
    session_id: str
    run_id: str
    answer: str
    evidence: list[EvidenceItem] = Field(default_factory=list)
    decision_trace: list[DecisionPoint] = Field(default_factory=list)
    retrieval_strategy: str | None = None
    faithfulness_score: float | None = None
    answer_relevance: float | None = None
    unsupported_claims: list[str] = Field(default_factory=list)
    graph_preview: dict | None = None


class ChatService:
    def __init__(self, supervisor: SupervisorAgent) -> None:
        self.supervisor = supervisor
        self.traces: OrderedDict[str, tuple[str, RunTrace]] = OrderedDict()
        self.lock = Lock()

    def record_trace(self, session_key: str, trace: RunTrace) -> None:
        with self.lock:
            self.traces[trace.run_id] = (session_key, trace)
            if len(self.traces) > 512:
                self.traces.popitem(last=False)

    def get_trace(self, run_id: str, session_key: str) -> RunTrace | None:
        with self.lock:
            entry = self.traces.get(run_id)
            if entry and entry[0] == session_key:
                return entry[1]
        return None


def get_chat_service(container: Annotated[AppContainer, Depends(get_app_container)]) -> ChatService:
    return container.chat_service


def chat_role(
    container: Annotated[AppContainer, Depends(get_app_container)],
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    configured = container.settings.chat_api_key
    if configured is None and container.settings.environment == "local" and not authorization:
        return "viewer"
    if configured is not None and authorization is not None:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer" and compare_digest(
            token.encode(), configured.get_secret_value().encode(),
        ) and token:
            return "admin"
    raise HTTPException(401, "Chat authentication required.", headers={"WWW-Authenticate": "Bearer"})


@router.post("", response_model=ChatResponse)
async def create_chat_completion(
    request: ChatRequest,
    http_request: Request,
    service: Annotated[ChatService, Depends(get_chat_service)],
    role: Annotated[str, Depends(chat_role)],
) -> ChatResponse:
    if not request.query.strip():
        raise HTTPException(400, "Query cannot be empty.")

    session_id = str(request.session_id or uuid4())
    session_key = f"{role}:{session_id}"
    result = await service.supervisor.run(
        query=request.query,
        session_id=session_key,
        history=[message.model_dump() for message in request.history],
        roles=[role],
        request_id=getattr(http_request.state, "request_id", None),
    )
    evidence = [
        EvidenceItem(**item.model_dump(), citation=f"Source {index}")
        for index, item in enumerate(result.evidence, start=1)
    ]
    trace = RunTrace(
        run_id=result.run_id,
        evidence=evidence,
        decision_trace=result.decision_trace,
        faithfulness_score=result.faithfulness_score,
        unsupported_claims=result.unsupported_claims,
        **result.metadata,
    )
    service.record_trace(session_key, trace)

    return ChatResponse(
        session_id=session_id,
        run_id=result.run_id,
        answer=result.final_answer,
        evidence=evidence,
        decision_trace=trace.decision_trace if request.include_decision_trace else [],
        retrieval_strategy=trace.retrieval_strategy,
        faithfulness_score=trace.faithfulness_score,
        answer_relevance=trace.answer_relevance,
        unsupported_claims=trace.unsupported_claims,
        graph_preview=(
            SubgraphBuilder().from_evidence(result.evidence) if request.include_graph_preview else None
        ),
    )


@router.get("/{session_id}/history")
async def get_chat_history(
    session_id: UUID4,
    service: Annotated[ChatService, Depends(get_chat_service)],
    role: Annotated[str, Depends(chat_role)],
) -> dict[str, Any]:
    return {
        "session_id": str(session_id),
        "messages": service.supervisor.memory.history(f"{role}:{session_id}"),
    }


@router.get("/runs/{run_id}/trace", response_model=RunTrace)
async def get_agent_run_trace(
    run_id: UUID,
    session_id: Annotated[UUID4, Header(alias="X-Session-ID")],
    service: Annotated[ChatService, Depends(get_chat_service)],
    role: Annotated[str, Depends(chat_role)],
) -> RunTrace:
    trace = service.get_trace(str(run_id), f"{role}:{session_id}")
    if trace is None:
        raise HTTPException(404, "Agent run not found.")
    return trace
