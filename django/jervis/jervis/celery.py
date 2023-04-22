import os
from celery import Celery
from telegram.tasks import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jervis.settings')

app = Celery('jervis',
             broker=f'redis://{os.getenv("REDIS_HOST")}:6379',
             backend=f'redis://{os.getenv("REDIS_HOST")}:6379',
             include=['jervis.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
