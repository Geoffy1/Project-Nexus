from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrRecruiterOrReadOnly(BasePermission):
    """
    Allow safe (GET, HEAD, OPTIONS) requests for everyone.
    Allow write (POST, PUT, PATCH, DELETE) only if the user is authenticated
    and is either:
      - a superuser
      - has role 'admin' or 'recruiter'
    """

    def has_permission(self, request, view):
        # Everyone can read
        if request.method in SAFE_METHODS:
            return True

        # Must be authenticated for write actions
        if not (request.user and request.user.is_authenticated):
            return False

        # Superusers always allowed
        if request.user.is_superuser:
            return True

        # Role-based access
        return request.user.role in ["admin", "recruiter"]



# from rest_framework.permissions import BasePermission, SAFE_METHODS


# class IsAdminOrRecruiterOrReadOnly(BasePermission):
#     """
#     Allow safe (GET, HEAD, OPTIONS) requests for everyone.
#     Allow write (POST, PUT, PATCH, DELETE) only if the user is authenticated
#     and has role 'admin' or 'recruiter'.
#     """

#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         return (
#             request.user
#             and request.user.is_authenticated
#             and request.user.role in ["admin", "recruiter"]
#         )
