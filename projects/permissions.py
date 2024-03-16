from rest_framework import permissions


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
    Permission pour permettre uniquement à l'auteur du projet de modifier ou de supprimer un contributeur.
    Les autres utilisateurs ont uniquement un accès en lecture.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.project.author == request.user