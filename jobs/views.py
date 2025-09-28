from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Job, Category
from .serializers import JobSerializer, CategorySerializer
from .permissions import IsAdminOrRecruiterOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrRecruiterOrReadOnly]
    lookup_field = "slug"


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAdminOrRecruiterOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ["category__slug", "location", "employment_type"]
    search_fields = ["title", "description", "company"]
    ordering_fields = ["created_at", "salary_min", "salary_max"]

    def get_queryset(self):
        qs = Job.objects.select_related("category", "posted_by").all()
        q = self.request.query_params.get("q")
        if q:
            vector = SearchVector("title", "description", "company")
            query = SearchQuery(q)
            qs = qs.annotate(rank=SearchRank(vector, query)) \
                   .filter(rank__gte=0.01).order_by("-rank")
        return qs

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


# from rest_framework import viewsets
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
# from .models import Job, Category
# from .serializers import JobSerializer, CategorySerializer
# from .permissions import IsAdminOrReadOnly

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminOrReadOnly]
#     lookup_field = "slug"

# class JobViewSet(viewsets.ModelViewSet):
#     serializer_class = JobSerializer
#     permission_classes = [IsAdminOrReadOnly]
#     filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
#     filterset_fields = ["category__slug", "location", "employment_type"]
#     search_fields = ["title", "description", "company"]
#     ordering_fields = ["created_at", "salary_min", "salary_max"]

#     def get_queryset(self):
#         qs = Job.objects.select_related("category", "posted_by").all()
#         q = self.request.query_params.get("q")
#         if q:
#             vector = SearchVector("title", "description", "company")
#             query = SearchQuery(q)
#             qs = qs.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.01).order_by("-rank")
#         return qs

#     def perform_create(self, serializer):
#         serializer.save(posted_by=self.request.user)
