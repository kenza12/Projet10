
from rest_framework import permissions, generics
from .serializers import SignupUserSerializer, UserSerializer
from .models import User
from issues.models import Issue, Comment
from projects.models import Project, Contributor
from .permissions import IsSelfOrAdmin
from rest_framework.permissions import IsAdminUser
from django.db import transaction


class SignupView(generics.CreateAPIView):
    """
    API view for user registration.

    Allows any user to sign up by creating a new user instance.
    """
    serializer_class = SignupUserSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    """
    API view for listing all users.

    Accessible only by admin users to see a list of all registered users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Override the default queryset to return all users for superusers.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.none()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a user instance.

    Users can manage their own data. Superusers can manage data of all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]

    def get_object(self):
        """
        Override to allow users to access their own information or superusers
        to access any user's information.
        """
        obj = super().get_object()
        if not (self.request.user.is_superuser or self.request.user == obj):
            raise permissions.PermissionDenied("You do not have permission to access this user.")
        return obj

    @transaction.atomic
    def perform_destroy(self, instance):
        """
        Custom destruction method to ensure all data related to the user is also deleted.
        """

        # Delete user's issues, comments and contributions
        Issue.objects.filter(author=instance).delete()
        Comment.objects.filter(author=instance).delete()
        Contributor.objects.filter(user=instance).delete()

        # Delete projects authored by the user
        projects = Project.objects.filter(author=instance)
        for project in projects:
            project.delete()

        # Finally, delete the user instance
        instance.delete()
