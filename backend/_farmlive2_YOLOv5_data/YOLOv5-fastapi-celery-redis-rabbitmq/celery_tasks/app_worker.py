import os
from celery import Celery

# BROKER_URI = 'amqp://rabbitmq'
BROKER_URI: str = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")

# BACKEND_URI = 'redis://redis'
BACKEND_URI = 'redis://localhost:6379/0'

app = Celery(
    'celery_tasks',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['celery_tasks.tasks']
)
