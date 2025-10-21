"""
URL configuration for jobboard project.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# App viewsets
from jobs.views import JobViewSet, CategoryViewSet
from applications.views import ApplicationViewSet


# ----------------------------------------
# 🏠 Custom Views
# ----------------------------------------

def home(request):
    """
    ✅ CHANGED: Now renders 'index.html' from templates directory.
    This replaces the previous JSON-only welcome.
    """
    return render(request, "index.html")  # <-- make sure index.html exists in BASE_DIR/templates/


def health_check(request):
    """✅ UNCHANGED: Used by Render to confirm uptime."""
    return JsonResponse({"status": "ok"})


# ----------------------------------------
# 🔗 API Router Setup
# ----------------------------------------

router = DefaultRouter()
router.register(r"jobs", JobViewSet, basename="job")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"applications", ApplicationViewSet, basename="application")


# ----------------------------------------
# 🌐 URL Patterns
# ----------------------------------------

urlpatterns = [
    path("", home, name="home"),                     # ✅ CHANGED: Root route serves template
    path("health/", health_check, name="health_check"),  # ✅ UNCHANGED

    # Admin panel
    path("admin/", admin.site.urls),

    # API endpoints
    path("api/", include(router.urls)),

    # Auth (JWT)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API documentation (Swagger)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]




# """
# URL configuration for jobboard project.
# """

# from django.contrib import admin
# from django.urls import path, include
# from django.shortcuts import render  # ✅ ADDED: to render HTML templates
# from django.http import JsonResponse
# from rest_framework.routers import DefaultRouter
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# # App viewsets
# from jobs.views import JobViewSet, CategoryViewSet
# from applications.views import ApplicationViewSet


# # ----------------------------------------
# # 🏠 Custom Views
# # ----------------------------------------

# # ✅ CHANGED: Previously returned JSON; now renders `index.html` for your animated homepage
# def home(request):
#     """
#     Renders the responsive animated landing page (index.html).
#     This replaces the old JSON welcome message.
#     """
#     return render(request, "index.html")


# # ✅ UNCHANGED: Still used for uptime checks on Render
# def health_check(request):
#     """Used by Render or monitoring tools to confirm the service is healthy."""
#     return JsonResponse({"status": "ok"})


# # ----------------------------------------
# # 🔗 API Router Setup (unchanged)
# # ----------------------------------------

# router = DefaultRouter()
# router.register(r"jobs", JobViewSet, basename="job")
# router.register(r"categories", CategoryViewSet, basename="category")
# router.register(r"applications", ApplicationViewSet, basename="application")


# # ----------------------------------------
# # 🌐 URL Patterns
# # ----------------------------------------

# urlpatterns = [
#     # ✅ CHANGED: Root route now serves the HTML homepage instead of JSON
#     path("", home, name="home"),

#     # ✅ UNCHANGED: Health check endpoint for Render
#     path("health/", health_check, name="health_check"),

#     # Django admin panel
#     path("admin/", admin.site.urls),

#     # REST API endpoints
#     path("api/", include(router.urls)),

#     # JWT Authentication endpoints
#     path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

#     # API Schema & Swagger Docs
#     path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
#     path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
# ]


# # """
# # URL configuration for jobboard project.
# # """

# # from django.contrib import admin
# # from django.urls import path, include
# # from rest_framework.routers import DefaultRouter
# # from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# # from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# # from django.http import JsonResponse

# # # Import your views
# # from jobs.views import JobViewSet, CategoryViewSet
# # from applications.views import ApplicationViewSet


# # # --- Custom Views ---

# # def home(request):
# #     """Provides a welcome message and API index at the root path."""
# #     return JsonResponse({
# #         "message": "Welcome to Project Nexus Job Board API",
# #         "endpoints": {
# #             "jobs": "/api/jobs/",
# #             "categories": "/api/categories/",
# #             "applications": "/api/applications/",
# #             "docs": "/api/docs/"
# #         }
# #     })

# # def health_check(request):
# #     """Used by monitoring tools (like Render) to confirm the service is running."""
# #     return JsonResponse({"status": "ok"})


# # # --- Router Setup ---

# # router = DefaultRouter()
# # router.register(r"jobs", JobViewSet, basename="job")
# # router.register(r"categories", CategoryViewSet, basename="category")
# # router.register(r"applications", ApplicationViewSet, basename="application")


# # # --- Main URL Patterns ---

# # urlpatterns = [
# #     # 1. Health/Root Check
# #     path("", home), # Root route should now work
# #     path("health/", health_check), # Health check route

# #     # 2. Django Admin
# #     path("admin/", admin.site.urls),

# #     # 3. REST API Routes
# #     path("api/", include(router.urls)),
    
# #     # 4. Auth & Docs
# #     path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
# #     path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
# #     path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
# #     path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
# # ]

# # # """
# # # URL configuration for jobboard project.

# # # The `urlpatterns` list routes URLs to views. For more information please see:
# # #     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# # # Examples:
# # # Function views
# # #     1. Add an import:  from my_app import views
# # #     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# # # Class-based views
# # #     1. Add an import:  from other_app.views import Home
# # #     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# # # Including another URLconf
# # #     1. Import the include() function: from django.urls import include, path
# # #     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# # # """

# # # from django.contrib import admin
# # # from django.urls import path, include
# # # from rest_framework.routers import DefaultRouter
# # # from jobs.views import JobViewSet, CategoryViewSet
# # # from applications.views import ApplicationViewSet
# # # from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# # # from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# # # from django.http import JsonResponse
# # # from django.http import JsonResponse
# # # #home or root added
# # # def home(request):
# # #     return JsonResponse({
# # #         "message": "Welcome to Project Nexus Job Board API",
# # #         "endpoints": {
# # #             "jobs": "/api/jobs/",
# # #             "categories": "/api/categories/",
# # #             "applications": "/api/applications/",
# # #             "docs": "/api/docs/"
# # #         }
# # #     })
# # # #end of home

# # # router = DefaultRouter()
# # # router.register(r"jobs", JobViewSet, basename="job")
# # # router.register(r"categories", CategoryViewSet, basename="category")
# # # router.register(r"applications", ApplicationViewSet, basename="application")

# # # urlpatterns = [
# # #     path("", home), #added root route to avoid error (Not Found The requested resource was not found on this server.)
# # #     path("admin/", admin.site.urls),
# # #     path("api/", include(router.urls)),
# # #     path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
# # #     path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
# # #     path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
# # #     path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
# # # ]


# # # def health_check(request):
# # #     return JsonResponse({"status": "ok"})

# # # urlpatterns = [
# # #     # existing paths
# # #     path("health/", health_check),
# # # ]
