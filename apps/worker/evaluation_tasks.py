from typing import Any

from apps.worker.celery_app import celery_app
from graphrag_system.evaluation.faithfulness import FaithfulnessEvaluator


@celery_app.task(name="apps.worker.evaluation_tasks.evaluate_answer_faithfulness", bind=True)
def evaluate_answer_faithfulness(self, answer_id: str, answer: str, contexts: list[str]) -> dict[str, Any]:
    result = FaithfulnessEvaluator().evaluate(answer, contexts)
    result["task_id"] = self.request.id
    result["answer_id"] = answer_id
    return result


@celery_app.task(name="apps.worker.evaluation_tasks.run_regression_evaluation", bind=True)
def run_regression_evaluation(self, dataset_name: str, metrics: list[str], sample_size: int | None = None) -> dict[str, Any]:
    return {
        "task_id": self.request.id,
        "status": "completed",
        "dataset_name": dataset_name,
        "metrics": metrics,
        "sample_size": sample_size,
        "summary": {},
    }
