from rest_framework import permissions
from projects.models import Project, Contributor


class IsIssueAuthorOrProjectContributor(permissions.BasePermission):
    """
    Permission qui permet uniquement aux contributeurs d'un projet de créer, voir, modifier 
    ou supprimer des issues.
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')

        if project_id:
            project = Project.objects.get(pk=project_id)
            # Vérifier si l'utilisateur est un contributeur du projet
            is_contributor = Contributor.objects.filter(project=project, user=request.user).exists()

            if view.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
                return is_contributor
        
        return True

    def has_object_permission(self, request, view, obj):
        # L'auteur de l'issue peut la modifier ou la supprimer
        if obj.author == request.user:
            return True

        # Seuls les contributeurs du projet peuvent lire l'issue
        if request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(project=obj.project, user=request.user).exists()

        return False

class IsCommentAuthorOrProjectContributor(permissions.BasePermission):
    """
    Permission permettant uniquement à l'auteur d'un commentaire de le modifier ou le supprimer.
    Les contributeurs du projet associé ont un accès en lecture seulement.
    Les utilisateurs non contributeurs n'ont aucun droit.
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')

        if project_id:
            project = Project.objects.get(pk=project_id)
            is_contributor = Contributor.objects.filter(project=project, user=request.user).exists()
            return is_contributor
        
        return True

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True

        if request.method in permissions.SAFE_METHODS:
            project = obj.issue.project
            return Contributor.objects.filter(project=project, user=request.user).exists()

        return False
