from rest_framework import serializers
from .models import Job, Category
from applications.models import Application

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, source="category", queryset=Category.objects.all(), required=False)
    posted_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = ["id","title","company","description","location","employment_type",
                  "salary_min","salary_max","category","category_id","posted_by","is_published","created_at"]

