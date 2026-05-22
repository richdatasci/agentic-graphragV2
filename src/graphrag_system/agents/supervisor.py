from graphrag_system.agents.evaluator_agent import EvaluatorAgent
from graphrag_system.agents.planner import PlannerAgent
from graphrag_system.agents.retriever_agent import RetrieverAgent
from graphrag_system.agents.state import AgentRunResult, DecisionPoint
from graphrag_system.agents.synthesiser import AnswerSynthesiser
from graphrag_system.llm.model_gateway import ModelGateway
from graphrag_system.retrieval.hybrid_retriever import HybridRetriever


class SupervisorAgent:
    def __init__(self, model_gateway: ModelGateway, retriever: HybridRetriever | None = None) -> None:
        self.model_gateway = model_gateway
        self.planner = PlannerAgent()
        self.retriever_agent = RetrieverAgent(retriever)
        self.synthesiser = AnswerSynthesiser(model_gateway)
        self.evaluator = EvaluatorAgent()

    async def run(self, query: str, session_id: str, history: list[dict] | None = None) -> AgentRunResult:
        decision_trace: list[DecisionPoint] = [
            DecisionPoint(
                step="start",
                decision="start_agent_run",
                reason="Received user query and created an agent run.",
                confidence=1.0,
            )
        ]

        strategy, plan_trace = self.planner.plan(query)
        decision_trace.extend(plan_trace)

        evidence, context, retrieval_decision = await self.retriever_agent.retrieve(query)
        decision_trace.append(retrieval_decision)

        answer = await self.synthesiser.synthesise(query, context)
        decision_trace.append(
            DecisionPoint(
                step="synthesise",
                decision="generated_grounded_answer",
                reason="Answer generated from packed retrieval context.",
                confidence=0.75,
            )
        )

        eval_result = self.evaluator.evaluate(answer, [item.text for item in evidence])
        unsupported = [c["claim"] for c in eval_result["claims"] if c["status"] == "unsupported"]
        decision_trace.append(
            DecisionPoint(
                step="evaluate",
                decision=eval_result["recommended_action"],
                reason="Faithfulness evaluation completed against retrieved context.",
                confidence=eval_result["faithfulness_score"],
            )
        )

        return AgentRunResult(
            session_id=session_id,
            final_answer=answer,
            evidence=evidence,
            decision_trace=decision_trace,
            faithfulness_score=eval_result["faithfulness_score"],
            unsupported_claims=unsupported,
            metadata={"retrieval_strategy": strategy},
        )
