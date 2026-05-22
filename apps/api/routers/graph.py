from typing import Any

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from graphrag_system.graph_presentation.subgraph_builder import SubgraphBuilder

router = APIRouter(prefix="/graph", tags=["graph"])


class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: str
    properties: dict[str, Any] = Field(default_factory=dict)


class SubgraphResponse(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)


@router.get("/entities/search")
async def search_entities(q: str = Query(..., min_length=1), limit: int = Query(default=25, ge=1, le=100)) -> dict[str, Any]:
    return {"query": q, "limit": limit, "results": []}


@router.get("/entities/{entity_id}/neighbours", response_model=SubgraphResponse)
async def get_entity_neighbours(entity_id: str, depth: int = Query(default=1, ge=1, le=3)) -> SubgraphResponse:
    subgraph = SubgraphBuilder().placeholder_neighbourhood(entity_id, depth)
    return SubgraphResponse(**subgraph)


@router.get("/path", response_model=SubgraphResponse)
async def get_path_between_entities(
    source: str = Query(..., min_length=1),
    target: str = Query(..., min_length=1),
    max_depth: int = Query(default=4, ge=1, le=8),
) -> SubgraphResponse:
    subgraph = SubgraphBuilder().placeholder_path(source, target)
    return SubgraphResponse(**subgraph)


@router.get("/subgraph", response_model=SubgraphResponse)
async def get_subgraph(entity_id: str = Query(..., min_length=1), depth: int = Query(default=2, ge=1, le=4)) -> SubgraphResponse:
    return SubgraphResponse(**SubgraphBuilder().placeholder_neighbourhood(entity_id, depth))


@router.get("/schema")
async def get_graph_schema() -> dict[str, Any]:
    return {
        "labels": ["Document", "Chunk", "Entity", "Claim", "Triple", "Source", "AgentRun", "ToolCall"],
        "relationship_types": ["CONTAINS", "MENTIONS", "SUPPORTS", "RELATED_TO", "DERIVED_FROM", "USED"],
        "indexes": [],
    }
