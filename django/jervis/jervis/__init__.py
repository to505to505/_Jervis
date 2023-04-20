from __future__ import absolute_import
import os
from celery import Celery

# Установите переменную окружения для проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jervis.settings')

app = Celery('jervis')

# Установите конфигурацию Celery из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузите все задачи из приложений Django
app.autodiscover_tasks()