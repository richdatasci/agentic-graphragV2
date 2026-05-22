from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from graphrag_system.evaluation.faithfulness import FaithfulnessEvaluator

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


class FaithfulnessRequest(BaseModel):
    answer: str = Field(..., min_length=1)
    contexts: list[str] = Field(..., min_length=1)


class ClaimEvaluation(BaseModel):
    claim: str
    status: Literal["supported", "partially_supported", "unsupported"]
    supporting_context_indexes: list[int] = Field(default_factory=list)
    notes: str | None = None


class FaithfulnessResponse(BaseModel):
    faithfulness_score: float
    claims: list[ClaimEvaluation] = Field(default_factory=list)
    recommended_action: str


@router.post("/faithfulness", response_model=FaithfulnessResponse)
async def evaluate_faithfulness(request: FaithfulnessRequest) -> FaithfulnessResponse:
    result = FaithfulnessEvaluator().evaluate(request.answer, request.contexts)
    return FaithfulnessResponse(**result)


@router.post("/runs")
async def create_evaluation_run(dataset_name: str, sample_size: int | None = None) -> dict[str, object]:
    return {"run_id": "eval_pending", "dataset_name": dataset_name, "sample_size": sample_size, "status": "queued"}


@router.get("/runs/{run_id}")
async def get_evaluation_run(run_id: str) -> dict[str, object]:
    return {"run_id": run_id, "status": "unknown", "summary": {}}
