from celery import Celery
from backend.core.config import REDIS_URL

celery = Celery(
    "sales_machine",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Mantém resultados por 24h
    result_expires=86400,
)
