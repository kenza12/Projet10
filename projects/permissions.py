from rest_framework import permissions
from .models import Project, Contributor


class IsProjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission pour permettre uniquement à l'auteur du projet de le modifier ou de le supprimer.
    Les autres utilisateurs ont uniquement un accès en lecture.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsProjectAuthorForContributor(permissions.BasePermission):
    """
    Permission qui permet uniquement à l'auteur du projet de créer, modifier ou supprimer
    des contributeurs. Les contributeurs du projet ont seulement le droit de lecture.
    Les autres utilisateurs n'ont aucun droit d'accès.
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)

        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            # Seul l'auteur du projet peut effectuer ces actions
            return request.user == project.author

        if view.action in ['list', 'retrieve']:
            # L'auteur et les contributeurs du projet ont le droit de lecture
            return (
                request.user == project.author or 
                Contributor.objects.filter(project=project, user=request.user).exists()
            )

        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            # Seul l'auteur du projet peut effectuer ces actions sur un objet contributeur
            return request.user == obj.project.author

        if view.action in ['retrieve']:
            # L'auteur et les contributeurs du projet peuvent voir les détails du contributeur
            return (
                request.user == obj.project.author or 
                Contributor.objects.filter(project=obj.project, user=request.user).exists()
            )

        return False
