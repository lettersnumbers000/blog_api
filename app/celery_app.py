from celery import Celery

from app.config import settings

celery_app = Celery("app", broker=settings.redis_url, backend=settings.redis_url, include=["app.tasks"])
celery_app.conf.task_always_eager = settings.celery_eager
