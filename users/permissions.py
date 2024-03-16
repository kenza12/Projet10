
from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permission personnalisée pour permettre aux superutilisateurs de gérer tous les profils,
    tandis que les utilisateurs réguliers ne peuvent gérer que leur propre profil.
    """
    def has_object_permission(self, request, view, obj):
        # Autoriser l'accès complet pour les superutilisateurs
        if request.user.is_superuser:
            return True
        # Autoriser l'accès complet uniquement à l'utilisateur concerné pour les autres
        return obj == request.user