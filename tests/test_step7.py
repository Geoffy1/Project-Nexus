from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class Step7JWTRoleFlowTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username="superadmin", email="super@example.com", password="SuperPass123!")
        self.recruiter = User.objects.create_user(username="recruiter1", email="rec@example.com", password="RecruiterPass123!")
        self.recruiter.role = "recruiter"
        self.recruiter.save()
        self.normal = User.objects.create_user(username="normaluser", email="user@example.com", password="UserPass123!")
        self.normal.role = "user"
        self.normal.save()
        self.client = APIClient()

    def get_token(self, username, password):
        resp = self.client.post("/api/auth/token/", {"username": username, "password": password}, format="json")
        return resp.data.get("access")

    def job_payload(self):
        return {
            "title": "Test Job",
            "company": "ACME",
            "description": "Test",
            "location": "Remote",
            "employment_type": "FT",
        }

    def test_superuser_can_create(self):
        token = self.get_token("superadmin", "SuperPass123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        resp = self.client.post("/api/jobs/", self.job_payload(), format="json")
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))

    def test_recruiter_can_create(self):
        token = self.get_token("recruiter1", "RecruiterPass123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        resp = self.client.post("/api/jobs/", self.job_payload(), format="json")
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))

    def test_normal_user_cannot_create(self):
        token = self.get_token("normaluser", "UserPass123!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        resp = self.client.post("/api/jobs/", self.job_payload(), format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_create(self):
        client = APIClient()
        resp = client.post("/api/jobs/", self.job_payload(), format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

