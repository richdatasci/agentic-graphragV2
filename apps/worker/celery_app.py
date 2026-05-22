import os

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "agentic_graphrag_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "apps.worker.ingestion_tasks",
        "apps.worker.embedding_tasks",
        "apps.worker.graph_tasks",
        "apps.worker.evaluation_tasks",
    ],
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=os.getenv("CELERY_TIMEZONE", "Europe/London"),
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    result_expires=86400,
    broker_connection_retry_on_startup=True,
)


@celery_app.task(name="apps.worker.celery_app.ping")
def ping() -> dict[str, str]:
    return {"status": "ok", "worker": "agentic_graphrag_worker"}
