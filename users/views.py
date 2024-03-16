from rest_framework import generics, viewsets, mixins, permissions
from .models import User
from .serializers import RegisterUserSerializer, UserSerializer
from .permissions import IsSelfOrAdmin


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    ViewSet pour la gestion des utilisateurs.
    Les superutilisateurs peuvent gérer tous les profils, les autres utilisateurs uniquement le leur.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]

    def get_queryset(self):
        # Si l'utilisateur est un superutilisateur, retourner tous les profils
        if self.request.user.is_superuser:
            return User.objects.all()
        # Sinon, retourner uniquement le profil de l'utilisateur connecté
        return User.objects.filter(id=self.request.user.id)

class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer