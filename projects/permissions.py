from rest_framework import permissions
from .models import Project, Contributor


class IsProjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a project to edit or delete it.
    Other users can only have read access.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access or modify the object.

        Args:
            request: The HTTP request.
            view: The view being accessed.
            obj: The project object being accessed or modified.

        Returns:
            bool: True if the request is a read-only request or if the user is the author of the project, False otherwise.
        """
        # Allow read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of the project
        return obj.author == request.user


class IsProjectAuthorForContributor(permissions.BasePermission):
    """
    Permission to allow only the author of the project to create, edit, or delete contributors.
    Contributors of the project can only read. Other users have no access.
    """
    def has_permission(self, request, view):
        """
        Check if the user has permission to access the contributors of a project.

        Args:
            request: The HTTP request.
            view: The view being accessed.

        Returns:
            bool: True if the user has the appropriate permissions, False otherwise.
        """
        project_id = view.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)

        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only the author of the project can perform these actions
            return request.user == project.author

        if view.action in ['list', 'retrieve']:
            # Both the author and the contributors of the project can read
            return (
                request.user == project.author or 
                Contributor.objects.filter(project=project, user=request.user).exists()
            )

        # Default to True for other cases
        return True

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform specific actions on a contributor object.

        Args:
            request: The HTTP request.
            view: The view being accessed.
            obj: The contributor object being accessed or modified.

        Returns:
            bool: True if the user has the appropriate permissions, False otherwise.
        """
        if view.action in ['update', 'partial_update', 'destroy']:
            # Only the author of the project can perform these actions on a contributor object
            return request.user == obj.project.author

        if view.action in ['retrieve']:
            # Both the author and the contributors of the project can view contributor details
            return (
                request.user == obj.project.author or 
                Contributor.objects.filter(project=obj.project, user=request.user).exists()
            )

        # Default to False for other cases
        return False
