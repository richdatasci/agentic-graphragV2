import asyncio
import json
import logging
from collections.abc import Mapping
from dataclasses import replace
from functools import partial
from time import perf_counter
from typing import TypedDict
from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from graphrag_system.agents.evaluator_agent import EvaluatorAgent
from graphrag_system.agents.governance_agent import GovernanceAgent
from graphrag_system.agents.memory_agent import MemoryAgent
from graphrag_system.agents.planner import PlannerAgent
from graphrag_system.agents.retriever_agent import RetrieverAgent
from graphrag_system.agents.state import AgentRunResult, AgentState, DecisionPoint
from graphrag_system.agents.synthesiser import AnswerSynthesiser
from graphrag_system.agents.tool_agent import ToolAgent
from graphrag_system.governance.audit_log import AuditLogger
from graphrag_system.llm.model_gateway import ModelGateway
from graphrag_system.retrieval.hybrid_retriever import HybridRetriever
from graphrag_system.tools.base import BaseTool
from graphrag_system.utils.hashing import stable_hash

logger = logging.getLogger(__name__)
NO_EVIDENCE = "I couldn't find enough accessible evidence to answer this question."
UNVERIFIED = "I couldn't verify an answer against the available evidence."


class WorkflowState(TypedDict):
    run: AgentState


class SupervisorAgent:
    def __init__(
        self,
        model_gateway: ModelGateway,
        retriever: HybridRetriever | None = None,
        *,
        memory: MemoryAgent | None = None,
        tools: Mapping[str, BaseTool] | None = None,
        search_tool: str | None = None,
    ) -> None:
        if search_tool is not None and search_tool not in (tools or {}):
            raise ValueError("The configured search tool must be registered.")
        self.planner = PlannerAgent()
        self.retriever_agent = RetrieverAgent(retriever)
        self.synthesiser = AnswerSynthesiser(model_gateway)
        self.evaluator = EvaluatorAgent()
        self.memory = memory or MemoryAgent()
        self.governance = GovernanceAgent()
        self.tools = ToolAgent(tools)
        self.search_tool = search_tool
        self.audit = AuditLogger()

        flow = StateGraph(WorkflowState)
        flow.add_node("plan", self._plan)
        flow.add_node("retrieve", self._retrieve)
        flow.add_node("synthesise", self._synthesise)
        flow.add_node("evaluate", self._evaluate)
        flow.add_edge(START, "plan")
        flow.add_conditional_edges("plan", lambda state: END if state["run"].final_answer else "retrieve", [END, "retrieve"])
        flow.add_conditional_edges("retrieve", lambda state: "synthesise" if state["run"].evidence else END, ["synthesise", END])
        flow.add_conditional_edges("synthesise", lambda state: "evaluate" if state["run"].draft_answer else END, ["evaluate", END])
        flow.add_conditional_edges("evaluate", lambda state: END if state["run"].final_answer else "synthesise", [END, "synthesise"])
        self.workflow = flow.compile()

    def _plan(self, state: WorkflowState) -> WorkflowState:
        run = state["run"]
        if not any(self.governance.rbac.has_permission(role, "read") for role in run.roles):
            return {"run": replace(
                run, final_answer=NO_EVIDENCE, decision_trace=[DecisionPoint(
                    step="governance", decision="blocked", reason="Read permission is required.",
                )],
            )}
        if not self.governance.safe_text(run.user_query):
            return {"run": replace(
                run,
                final_answer="I can't process this request as a search question.",
                decision_trace=[DecisionPoint(
                    step="governance", decision="blocked", reason="Detected a control directive.",
                )],
            )}
        strategy, decisions = self.planner.plan(run.user_query)
        query = self.memory.contextualise(run.user_query, run.history)
        return {"run": replace(run, retrieval_strategy=strategy, rewritten_query=query, decision_trace=decisions)}

    async def _retrieve(self, state: WorkflowState) -> WorkflowState:
        run = state["run"]
        agent = self.retriever_agent
        query = run.rewritten_query
        evidence_filter = partial(
            self.governance.filter_evidence, roles=run.roles, preserve_policy=True,
        )
        evidence, statuses = await agent.search(
            query, run.retrieval_strategy, top_k=16, evidence_filter=evidence_filter,
        )
        allowed = self.governance.filter_evidence(evidence, run.roles)
        decisions = list(run.decision_trace)
        if not allowed and run.retrieval_strategy != "hybrid":
            remaining = {name: search for name, search in agent.routes(evidence_filter).items() if name not in statuses}
            evidence, fallback = await agent.retriever.search(query, remaining, top_k=16)
            allowed = self.governance.filter_evidence(evidence, run.roles)
            statuses.update(fallback)
            decisions.append(DecisionPoint(
                step="retrieve", decision="broaden_retrieval",
                reason="The selected route returned no eligible evidence.",
            ))
        calls = []
        if not allowed and self.search_tool and any(
            self.governance.rbac.has_permission(role, "read") for role in run.roles
        ):
            items, call = await self.tools.retrieve(self.search_tool, query, top_k=8)
            allowed = self.governance.filter_evidence(items, run.roles)
            calls.append({**call, "result_count": len(allowed), "reason": "Local evidence was unavailable."})

        packed, context = agent.retriever.packer.pack_evidence(agent.retriever.rank(query, allowed, 8))
        decisions.append(DecisionPoint(
            step="retrieve", decision="packed_evidence" if packed else "no_evidence",
            reason=f"Packed {len(packed)} eligible sources. Backends: " + ", ".join(
                f"{name}={status}" for name, status in statuses.items()
            ),
        ))
        return {"run": replace(
            run, evidence=packed, context=context, backends=statuses,
            tool_calls=calls, decision_trace=decisions,
            final_answer="" if packed else NO_EVIDENCE,
        )}

    async def _synthesise(self, state: WorkflowState) -> WorkflowState:
        run = state["run"]
        try:
            answer = await asyncio.wait_for(
                self.synthesiser.synthesise(
                    run.user_query, run.context, run.history, retry=bool(run.attempts),
                ),
                timeout=30,
            )
            answer = self.governance.redact(answer) if len(answer) <= 6000 else ""
        except Exception as error:  # noqa: BLE001
            logger.warning("agent_synthesis_failed error_type=%s", type(error).__name__)
            answer = ""
        accepted = bool(answer and self.governance.safe_text(answer))
        decision = DecisionPoint(
            step="synthesise", decision="draft_created" if accepted else "draft_unavailable",
            reason="Requested a cited answer from the packed sources.",
        )
        return {"run": replace(
            run, attempts=run.attempts + 1, draft_answer=answer if accepted else "",
            final_answer="" if accepted else UNVERIFIED,
            decision_trace=[*run.decision_trace, decision],
        )}

    def _evaluate(self, state: WorkflowState) -> WorkflowState:
        run = state["run"]
        result = self.evaluator.evaluate(
            run.draft_answer, [item.text for item in run.evidence], run.user_query,
        )
        passed = result["recommended_action"] == "allow"
        decision = "allow" if passed else "regenerate" if run.attempts < 2 else "withhold"
        point = DecisionPoint(
            step="evaluate", decision=decision,
            reason="Checked claims against their cited sources using the lexical evaluator.",
            confidence=result["faithfulness_score"],
        )
        return {"run": replace(
            run, evaluation=result, decision_trace=[*run.decision_trace, point],
            final_answer=run.draft_answer if passed else UNVERIFIED if run.attempts >= 2 else "",
        )}

    async def run(
        self, query: str, session_id: str, history: list[dict] | None = None,
        *, roles: list[str] | None = None, request_id: str | None = None,
    ) -> AgentRunResult:
        start = perf_counter()
        run_id = str(uuid4())
        query = self.governance.redact(query.strip())
        context = [
            {"role": item["role"], "content": self.governance.redact(item["content"])}
            for item in self.memory.context(session_id, history or [])
            if self.governance.safe_text(item["content"])
        ]
        state = await self.workflow.ainvoke({"run": AgentState(
            session_id=session_id, user_query=query, history=context,
            roles=["viewer"] if roles is None else roles,
        )})
        run = state["run"]
        if run.decision_trace[0].step != "governance":
            self.memory.record_turn(session_id, query, run.final_answer)
        metadata = {
            "retrieval_strategy": run.retrieval_strategy,
            "intent": {
                "hybrid": "general_question", "graph": "graph_navigation",
                "keyword": "exact_lookup", "vector": "semantic_lookup",
            }.get(run.retrieval_strategy, "general_question"),
            "retrieval_backends": run.backends,
            "tool_calls": run.tool_calls,
            "answer_relevance": run.evaluation.get("answer_relevance"),
            "duration_ms": round((perf_counter() - start) * 1000, 1),
        }
        audit = self.audit.log("chat", "agent_run", run_id, {
            "request_id": request_id, "session_hash": stable_hash(session_id), **metadata,
            "decisions": [point.decision for point in run.decision_trace],
        })
        logger.info("agent_run_completed %s", json.dumps(audit))
        return AgentRunResult(
            session_id=session_id, run_id=run_id, final_answer=run.final_answer,
            evidence=run.evidence, decision_trace=run.decision_trace,
            faithfulness_score=run.evaluation.get("faithfulness_score"),
            unsupported_claims=[
                claim["claim"] for claim in run.evaluation.get("claims", [])
                if claim["status"] != "supported"
            ],
            metadata=metadata,
        )
