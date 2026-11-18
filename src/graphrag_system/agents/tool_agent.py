import asyncio
import logging
from collections.abc import Mapping
from time import perf_counter

from graphrag_system.governance.safety_filters import SafetyFilter
from graphrag_system.retrieval.vector_retriever import RetrievedEvidence
from graphrag_system.tools.base import BaseTool

logger = logging.getLogger(__name__)


class ToolAgent:
    def __init__(self, tools: Mapping[str, BaseTool] | None = None) -> None:
        self.tools = dict(tools or {})
        self.safety = SafetyFilter()

    def call(self, tool_name: str, **kwargs):
        tool = self.tools.get(tool_name)
        if tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")
        return tool.run(**kwargs)

    async def retrieve(
        self, tool_name: str, query: str, top_k: int,
    ) -> tuple[list[RetrievedEvidence], dict]:
        """Run a server-selected search adapter with bounded, typed inputs and outputs."""
        trace = {"tool": tool_name, "top_k": top_k, "status": "blocked", "result_count": 0}
        if not self.safety.is_safe_tool_request(query):
            return [], trace
        start = perf_counter()
        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(self.call, tool_name, query=query, top_k=top_k),
                timeout=5,
            )
            if not isinstance(result, list):
                raise TypeError("Search tools must return an evidence list.")
            evidence = [RetrievedEvidence.model_validate(item) for item in result[:top_k]]
            trace.update(status="ok", result_count=len(evidence))
            return evidence, trace
        except Exception as error:  # noqa: BLE001
            trace.update(status="timeout" if isinstance(error, TimeoutError) else "failed")
            logger.warning("agent_tool_failed tool=%s error_type=%s", tool_name, type(error).__name__)
            return [], trace
        finally:
            trace["duration_ms"] = round((perf_counter() - start) * 1000, 1)
