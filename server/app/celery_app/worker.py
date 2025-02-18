import os
from celery import Celery

from config.settings import settings

app = Celery(
    'celery_app',
    broker=settings.celery_broker_url,
    backend=settings.celery_broker_url,
    include=['celery_app.tasks']
)