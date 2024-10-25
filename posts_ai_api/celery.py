import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "posts_ai_api.settings")

app = Celery("posts_ai_api", broker_connection_retry_on_startup=True)

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
