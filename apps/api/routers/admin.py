from typing import Any

from fastapi import APIRouter, Depends

from apps.api.dependencies import AppContainer, get_app_container

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/status")
async def get_platform_status(container: AppContainer = Depends(get_app_container)) -> dict[str, Any]:
    readiness = await container.readiness_check()
    return {"service": "Agentic GraphRAG API", "ready": readiness["ready"], "checks": readiness["checks"]}


@router.get("/config")
async def get_safe_config(container: AppContainer = Depends(get_app_container)) -> dict[str, Any]:
    s = container.settings
    return {
        "environment": s.environment,
        "log_level": s.log_level,
        "neo4j_uri": s.neo4j_uri,
        "qdrant_url": s.qdrant_url,
        "redis_url": s.redis_url,
        "minio_endpoint": s.minio_endpoint,
        "ollama_base_url": s.ollama_base_url,
        "default_llm_provider": s.default_llm_provider,
        "default_llm_model": s.default_llm_model,
        "default_embedding_model": s.default_embedding_model,
    }


@router.get("/metrics")
async def get_metrics_placeholder() -> dict[str, Any]:
    return {"requests_total": None, "agent_runs_total": None, "ingestion_jobs_total": None}
