from celery import shared_task
from .models import Job

@shared_task
def expire_old_jobs():
    Job.objects.filter(is_published=True, created_at__lt=... ).update(is_published=False)

