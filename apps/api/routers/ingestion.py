from typing import Any, Literal

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

from apps.api.dependencies import AppContainer, get_app_container
from graphrag_system.ingestion.pipeline import IngestionPipeline
from graphrag_system.utils.ids import new_id

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


class IngestionJobRequest(BaseModel):
    source_type: Literal["local_file", "sharepoint", "confluence", "google_drive", "sql", "rest_api", "web", "object_store"]
    source_uri: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    run_ocr: bool = True
    run_vlm_extraction: bool = True
    build_graph: bool = True
    build_vector_index: bool = True


class IngestionJobResponse(BaseModel):
    job_id: str
    status: str
    message: str
    result: dict[str, Any] | None = None


@router.post("/jobs", response_model=IngestionJobResponse)
async def create_ingestion_job(
    request: IngestionJobRequest,
    container: AppContainer = Depends(get_app_container),
) -> IngestionJobResponse:
    if request.source_type != "local_file" and not request.source_uri:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="source_uri is required.")

    # Local-safe synchronous baseline. Celery worker tasks are also included for async production mode.
    result = IngestionPipeline().ingest_source(request.model_dump())
    return IngestionJobResponse(
        job_id=new_id("job"),
        status=result.get("status", "completed"),
        message="Ingestion processed using local baseline pipeline.",
        result=result,
    )


@router.post("/files", response_model=IngestionJobResponse)
async def upload_file_for_ingestion(
    file: UploadFile = File(...),
    container: AppContainer = Depends(get_app_container),
) -> IngestionJobResponse:
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file must have a filename.")

    raw = await file.read()
    text = raw.decode("utf-8", errors="ignore")
    payload = {
        "filename": file.filename,
        "content_type": file.content_type,
        "document_id": f"doc_{file.filename}",
        "object_store_key": f"uploads/{file.filename}",
        "text": text,
        "metadata": {},
    }
    result = IngestionPipeline().ingest_uploaded_file(payload)
    return IngestionJobResponse(
        job_id=new_id("job"),
        status=result.get("status", "completed"),
        message="Uploaded file processed using local baseline pipeline.",
        result=result,
    )


@router.get("/jobs/{job_id}")
async def get_ingestion_job(job_id: str) -> dict[str, Any]:
    return {"job_id": job_id, "status": "completed_or_unknown"}
