# celery_main.py
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communication_service.settings')

BROKER_URL = f'redis://localhost:6379/0' # only for tests 'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
app = Celery('async_tasks', broker=BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()
app.conf.result_backend = 'redis://localhost:6379/0'

app.conf.update(
    task_serializer='json',
    timezone='Europe/Kiev',
    enable_utc=True,
    result_serializer='json',
    logfile='celery.log',
    loglevel='INFO'
)

