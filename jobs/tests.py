import pytest
from rest_framework.test import APIClient
from accounts.models import User
from jobs.models import Job, Category

@pytest.mark.django_db
def test_public_job_list():
    client = APIClient()
    cat = Category.objects.create(name="Engineering", slug="engineering")
    user = User.objects.create_user(username="u1", password="pass")
    Job.objects.create(title="Backend Dev", company="X", description="...", location="Nairobi", category=cat, employment_type="FT", posted_by=user)
    resp = client.get("/api/jobs/")
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
    assert data["results"][0]["title"] == "Backend Dev"
