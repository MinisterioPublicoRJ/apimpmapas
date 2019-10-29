from celery import Celery
from decouple import config


app = Celery(
    config('BROKER_QUEUE', 'lupa'),
    broker=config('BROKER_URL', default='redis://localhost:6379')
)
app.conf.timezone = 'UTC'
app.conf.task_default_queue = config('CELERY_TASK_QUEUE', None)
