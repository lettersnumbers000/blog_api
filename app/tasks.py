import logging

from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def notify_post_created(post_id: int, username: str) -> str:
    message = f"User {username} created post {post_id}"
    logger.info(message)
    return message
