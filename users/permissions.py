
from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    A custom permission class to allow superusers to manage all profiles,
    while regular users can only manage their own.
    """
    def has_object_permission(self, request, view, obj):
        """
        Checks whether the request has permission to act on the given object.

        Args:
            request: The HTTP request.
            view: The view which is being accessed.
            obj: The object being accessed or modified.

        Returns:
            bool: True if the user is a superuser or if the obj belongs to the user, False otherwise.
        """

        if request.user.is_superuser:
            return True
        return obj == request.user