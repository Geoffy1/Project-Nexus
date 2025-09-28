from django.db import models
from django.conf import settings
from jobs.models import Job

class Application(models.Model):
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    resume_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("applicant", "job")
        ordering = ["-created_at"]


# from django.db import models
# from django.conf import settings
# from jobs.models import Job

# class Application(models.Model):
#     applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
#     cover_letter = models.TextField(blank=True)
#     resume_url = models.URLField(blank=True)  # or FileField if storing files
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("applicant", "job")
#         ordering = ["-created_at"]

