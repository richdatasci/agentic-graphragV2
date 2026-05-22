from typing import Any

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from graphrag_system.graph_presentation.triples_preview import TriplePreviewService

router = APIRouter(prefix="/triples", tags=["triples"])


class TriplePreview(BaseModel):
    id: str
    subject: str
    predicate: str
    object: str
    confidence: float | None = None
    source_document_id: str | None = None
    chunk_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TripleSearchResponse(BaseModel):
    query: str
    results: list[TriplePreview] = Field(default_factory=list)


@router.get("/search", response_model=TripleSearchResponse)
async def search_triples(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=25, ge=1, le=100),
    min_confidence: float | None = Query(default=None, ge=0.0, le=1.0),
) -> TripleSearchResponse:
    service = TriplePreviewService()
    triples = service.search(q, limit=limit, min_confidence=min_confidence)
    return TripleSearchResponse(query=q, results=[TriplePreview(**t) for t in triples])


@router.get("/{triple_id}", response_model=TriplePreview)
async def get_triple(triple_id: str) -> TriplePreview:
    return TriplePreview(id=triple_id, subject="unknown", predicate="unknown", object="unknown")
