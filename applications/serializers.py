from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Application
        fields = ["id", "applicant", "job", "cover_letter", "resume_url", "created_at"]
        read_only_fields = ["applicant"]
