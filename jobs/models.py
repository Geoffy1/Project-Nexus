from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    EMPLOYMENT_TYPE = [
        ("FT", "Full-time"),
        ("PT", "Part-time"),
        ("CT", "Contract"),
        ("IN", "Internship"),
        ("RM", "Remote"),
    ]

    title = models.CharField(max_length=255, db_index=True)
    company = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, db_index=True)  # e.g., "Nairobi, Kenya"
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name="jobs")
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE, db_index=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs")
    is_published = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["location"]),
            models.Index(fields=["employment_type"]),
            GinIndex(fields=["title", "description"], name="job_search_gin"),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} @ {self.company}"

