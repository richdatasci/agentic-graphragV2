from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from apps.api.dependencies import AppContainer, get_app_container
from apps.api.middleware import register_middleware
from apps.api.routers import admin, chat, documents, evaluation, graph, ingestion, triples
from graphrag_system.config.logging import configure_logging

APP_NAME = "Agentic GraphRAG API"
APP_VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    container = get_app_container()
    configure_logging(container.settings.log_level)
    app.state.container = container
    await container.startup()
    try:
        yield
    finally:
        await container.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        description="Production-oriented Agentic GraphRAG API.",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    register_middleware(app)

    app.include_router(chat.router)
    app.include_router(ingestion.router)
    app.include_router(documents.router)
    app.include_router(graph.router)
    app.include_router(triples.router)
    app.include_router(evaluation.router)
    app.include_router(admin.router)

    @app.get("/", tags=["system"])
    async def root() -> JSONResponse:
        return JSONResponse(
            {
                "service": APP_NAME,
                "version": APP_VERSION,
                "status": "running",
                "docs": "/docs",
                "health": "/health",
                "quickstart": "See QUICKSTART.md",
            }
        )

    @app.get("/health", tags=["system"])
    async def health(container: Annotated[AppContainer, Depends(get_app_container)]) -> JSONResponse:
        return JSONResponse(
            {
                "status": "ok",
                "service": APP_NAME,
                "version": APP_VERSION,
                "environment": container.settings.environment,
            }
        )

    @app.get("/ready", tags=["system"])
    async def readiness(container: Annotated[AppContainer, Depends(get_app_container)]) -> JSONResponse:
        report = await container.readiness_check()
        return JSONResponse(report, status_code=200 if report["ready"] else 503)

    return app


app = create_app()
