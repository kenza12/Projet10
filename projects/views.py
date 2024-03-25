from rest_framework import viewsets, permissions
from .models import Project, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorCreateSerializer, ContributorListSerializer
from .permissions import IsProjectAuthorOrReadOnly, IsProjectAuthorForContributor
from django.shortcuts import get_object_or_404


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling project operations including create, read, update, and delete.

    This ViewSet uses different serializers for detail and list actions and filters the queryset
    based on the logged-in user's role as an author or a contributor.
    """
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsProjectAuthorOrReadOnly]

    def get_serializer_class(self):
        """
        Select the appropriate serializer based on the action.
        """
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectListSerializer

    def get_queryset(self):
        """
        Filter the queryset based on the logged-in user's association with the projects.
        """
        user = self.request.user
        return self.queryset.filter(
            contributors__user=user
        ).distinct() | self.queryset.filter(author=user).distinct()

    def perform_create(self, serializer):
        """
        Customize the creation of a project. The author of the project is automatically added as a contributor.
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=project.author, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing contributors in projects.

    It allows project authors and contributors to list, create, update, and delete contributors
    in a specific project.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorListSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectAuthorForContributor]

    def get_serializer_class(self):
        """
        Use different serializers for list and create actions.
        """
        if self.action in ['list', 'retrieve']:
            return ContributorListSerializer
        return ContributorCreateSerializer

    def get_queryset(self):
        """
        Filter contributors based on the project ID if it is present in the URL.
        """
        project_pk = self.kwargs.get('project_pk')
        if project_pk:
            return self.queryset.filter(project_id=project_pk)
        return self.queryset

    def perform_create(self, serializer):
        """
        Handle the creation of a new contributor. Automatically associates the contributor with the specified project.
        """
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)

        # Update the serializer context to include the project
        serializer.context['project'] = project

        # Save the contributor with the associated project
        serializer.save()