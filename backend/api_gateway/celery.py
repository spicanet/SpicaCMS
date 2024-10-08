# backend/api_gateway/celery.py

import os
from celery import Celery
from django.conf import settings
import logging.config

# Import Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_gateway.settings')

app = Celery('api_gateway')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Set up logging
logging.config.dictConfig(settings.LOGGING)