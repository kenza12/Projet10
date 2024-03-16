from rest_framework import permissions
from projects.models import Project

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission pour permettre uniquement à l'auteur de modifier ou supprimer une ressource.
    Les autres utilisateurs ont uniquement un accès en lecture.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsContributorOrReadOnly(permissions.BasePermission):
    """
    Permission pour permettre uniquement aux contributeurs du projet associé un accès en lecture.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        project = obj.project if hasattr(obj, 'project') else obj
        return project.contributors.filter(user=request.user).exists()