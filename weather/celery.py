import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')

app = Celery('weather')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    BROKER_URL = 'redis://127.0.0.1:6379/0',
)