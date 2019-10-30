import os

from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mprj_api.settings')

app = Celery(
    config('BROKER_QUEUE', 'lupa'),
    broker=config('BROKER_URL', default='redis://localhost:6379')
)
app.conf.timezone = 'UTC'
app.conf.task_default_queue = config('CELERY_TASK_QUEUE', None)
app.conf.event_serializer = 'pickle'
app.conf.task_serializer = 'pickle'
app.conf.accept_content = ['pickle']
