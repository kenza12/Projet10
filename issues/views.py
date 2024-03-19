from rest_framework import viewsets, permissions
from .models import Issue, Comment
from projects.models import Project, Contributor
from .serializers import IssueSerializer, CommentSerializer
from .permissions import IsIssueAuthorOrProjectContributor, IsCommentAuthorOrProjectContributor
from rest_framework.exceptions import NotFound


class IssueViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing issue instances.
    
    Attributes:
        queryset (QuerySet): QuerySet that contains all issues with their related project.
        serializer_class (IssueSerializer): The serializer that handles issue instances.
        permission_classes (list): List of permissions that apply to the viewset which includes
                                   authentication and issue-specific permissions.
                                   
    """
    queryset = Issue.objects.select_related('project').all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsIssueAuthorOrProjectContributor]

    def get_queryset(self):
        """
        Returns a filtered queryset of issues belonging to a specific project, identified by the URL parameter.
        """
        project_pk = self.kwargs.get('project_pk')
        if project_pk:
            return self.queryset.filter(project_id=project_pk)
        raise NotFound("Project not found.")

    def perform_create(self, serializer):
        """
        Performs the creation of a new Issue instance. Assigns the issue's author to the current user
        and the issue's project to the one specified in the URL parameter 'project_pk'.
        """
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        serializer.save(author=self.request.user, project=project)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('issue', 'issue__project').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthorOrProjectContributor]

    def get_queryset(self):
        issue_pk = self.kwargs.get('issue_pk')
        project_pk = self.kwargs.get('project_pk')
        if issue_pk and project_pk:
            return self.queryset.filter(issue_id=issue_pk, issue__project_id=project_pk)
        raise NotFound("Projet ou Issue non trouvé.")

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs.get('issue_pk'), project_id=self.kwargs.get('project_pk'))
        serializer.save(author=self.request.user, issue=issue)