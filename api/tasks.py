from weather.celery import app
from django.test import Client
from django.core.cache import cache


@app.task
def reboot_cache_main():
    res = cache.keys('*main*')
    if res:
        delete_cache = cache.delete_many(res)
    c = Client()
    response = c.get('/', SERVER_NAME='127.0.0.1:8000')