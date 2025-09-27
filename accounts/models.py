from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_USER = "user"
    ROLE_ADMIN = "admin"
    ROLE_RECRUITER = "recruiter"
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ADMIN, "Admin"),
        (ROLE_RECRUITER, "Recruiter"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)

