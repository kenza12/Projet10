from rest_framework import viewsets, permissions
from .models import Project, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorCreateSerializer, ContributorListSerializer
from .permissions import IsProjectAuthorOrReadOnly, IsProjectAuthorForContributor
from django.shortcuts import get_object_or_404


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets. Permet aux auteurs de projets de les modifier
    ou de les supprimer. Les contributeurs et les autres utilisateurs ont un accès en lecture seulement.
    """
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsProjectAuthorOrReadOnly]

    def get_serializer_class(self):
        # Sélectionner le bon serializer en fonction de l'action
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectListSerializer

    def get_queryset(self):
        # Filtrer les projets en fonction de l'utilisateur connecté
        user = self.request.user
        return self.queryset.filter(
            contributors__user=user
        ).distinct() | self.queryset.filter(author=user).distinct()

    def perform_create(self, serializer):
        # L'auteur du projet est automatiquement défini comme contributeur
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=project.author, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des contributeurs des projets. 
    Permet aux auteurs et aux contributeurs d'un projet d'accéder, de créer, 
    de modifier et de supprimer des contributeurs.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorListSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectAuthorForContributor]

    def get_serializer_class(self):
        # Utiliser des serializers différents selon l'action
        if self.action in ['list', 'retrieve']:
            return ContributorListSerializer
        return ContributorCreateSerializer

    def get_queryset(self):
        # Filtrer les contributeurs par projet si 'project_pk' est présent dans l'URL
        project_pk = self.kwargs.get('project_pk')
        if project_pk:
            return self.queryset.filter(project_id=project_pk)
        return self.queryset

    def perform_create(self, serializer):
        """
        Perform creation of a contributor. Automatically associates the contributor with the project based on the URL.

        Args:
            serializer (ContributorCreateSerializer): Serializer instance used for creating the contributor.
        """
        project_pk = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_pk)

        # Mettre à jour le contexte du serializer pour inclure le projet
        serializer.context['project'] = project

        # Enregistrer le contributeur avec le projet associé
        serializer.save()