# import os
# from celery import Celery

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobboard.settings")
# app = Celery("jobboard")
# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks()

# jobboard/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobboard.settings")

app = Celery("jobboard")
app.config_from_object("django.conf:settings", namespace="CELERY")

# This makes Django apps with tasks.py auto-register
app.autodiscover_tasks()
