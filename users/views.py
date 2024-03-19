
from rest_framework import permissions, generics
from .serializers import SignupUserSerializer, UserSerializer
from .models import User
from .permissions import IsSelfOrAdmin
from rest_framework.permissions import IsAdminUser



class SignupView(generics.CreateAPIView):
    serializer_class = SignupUserSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        This view should return a list of all the users
        for the currently authenticated admin user.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.none()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]

    def get_object(self):
        """
        Override the method to handle self retrieval and ensure that users
        can only access their own information unless they are superusers.
        """
        obj = super().get_object()
        if self.request.user.is_superuser or self.request.user == obj:
            return obj
        raise permissions.PermissionDenied()