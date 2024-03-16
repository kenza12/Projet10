from rest_framework import viewsets, permissions
from .models import Project, Contributor
from .serializers import ProjectListSerializer, ProjectDetailSerializer, ContributorCreateSerializer, ContributorListSerializer
from .permissions import IsProjectAuthorOrReadOnly, IsProjectAuthorForContributor


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets.
    Permet aux auteurs de projets de les modifier ou de les supprimer.
    Les contributeurs et les autres utilisateurs ont un accès en lecture seulement.
    """
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsProjectAuthorOrReadOnly]
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        user_id_param = self.request.query_params.get('user_id')
        if user_id_param and int(user_id_param) != user.id:
            return Project.objects.none()
        return Project.objects.filter(
            contributors__user=user
        ).distinct() | Project.objects.filter(author=user).distinct()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=project.author, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des contributeurs des projets. Permet de créer, lire, modifier et supprimer des contributeurs.
    Le contributeur d'un projet (différent de l'auteur) n'aura que le droit de lecture.
    """
    queryset = Contributor.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsProjectAuthorForContributor]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ContributorCreateSerializer
        return ContributorListSerializer

    def perform_create(self, serializer):
        # project = serializer.validated_data.get('project')
        # if self.request.user != project.author:
        #     raise permissions.PermissionDenied('Seul l’auteur du projet peut ajouter des contributeurs.')
        # if Contributor.objects.filter(project=project, user=serializer.validated_data.get('user')).exists():
        #     raise serializers.ValidationError('Cet utilisateur est déjà contributeur du projet.')
        serializer.save()
    
    def get_serializer_context(self):
        """
        Retourne le contexte pour le serializer. Ajoute l'utilisateur actuel au contexte.
        """
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}
