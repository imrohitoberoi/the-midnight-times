from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admins to access views.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
