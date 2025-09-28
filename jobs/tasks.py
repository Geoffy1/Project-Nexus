# jobs/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Job

@shared_task
def expire_jobs_older_than(days=30):
    cutoff = timezone.now() - timezone.timedelta(days=days)
    Job.objects.filter(created_at__lt=cutoff).update(is_active=False)
    return f"Expired jobs older than {days} days"
