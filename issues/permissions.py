from rest_framework import permissions
from projects.models import Project, Contributor


class IsIssueAuthorOrProjectContributor(permissions.BasePermission):
    """
    Custom permission class for issues.

    This permission allows only the contributors of a project to create, view,
    update, or delete issues related to that project. Additionally, it allows
    issue authors to modify or delete their own issues.
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')

        if project_id:
            project = Project.objects.get(pk=project_id)
            # Check if the user is a contributor to the project
            is_contributor = Contributor.objects.filter(project=project, user=request.user).exists()

            if view.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
                return is_contributor
        
        # Default to True to allow access when project_id is not present
        return True

    def has_object_permission(self, request, view, obj):
        # Issue authors can always modify or delete their issue
        if obj.author == request.user:
            return True

        # Contributors of the project can read (GET, HEAD, OPTIONS) the issue
        if request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(project=obj.project, user=request.user).exists()

        # Default deny
        return False


class IsCommentAuthorOrProjectContributor(permissions.BasePermission):
    """
    Custom permission class for comments.

    This permission allows only the author of a comment to modify or delete it.
    Contributors of the associated project have read-only access to the comment.
    Non-contributors have no access rights.
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')

        # If project_id is present, check if user is a contributor
        if project_id:
            project = Project.objects.get(pk=project_id)
            is_contributor = Contributor.objects.filter(project=project, user=request.user).exists()
            return is_contributor
        
        # Default to True to allow access when project_id is not present
        return True

    def has_object_permission(self, request, view, obj):
        # Comment authors can modify or delete their comments
        if obj.author == request.user:
            return True

        # Contributors of the project can read the comment
        if request.method in permissions.SAFE_METHODS:
            project = obj.issue.project
            return Contributor.objects.filter(project=project, user=request.user).exists()

        # Default deny
        return False
