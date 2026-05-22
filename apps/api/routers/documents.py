from typing import Any, Literal

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentSummary(BaseModel):
    id: str
    title: str
    source_type: str
    status: Literal["pending", "processing", "indexed", "failed"]
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    id: str
    document_id: str
    text: str
    page_number: int | None = None
    token_count: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


@router.get("", response_model=list[DocumentSummary])
async def list_documents(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    status_filter: str | None = Query(default=None, alias="status"),
) -> list[DocumentSummary]:
    return []


@router.get("/{document_id}", response_model=DocumentSummary)
async def get_document(document_id: str) -> DocumentSummary:
    return DocumentSummary(id=document_id, title="Document store pending", source_type="unknown", status="pending")


@router.get("/{document_id}/chunks", response_model=list[DocumentChunk])
async def get_document_chunks(document_id: str) -> list[DocumentChunk]:
    return []
