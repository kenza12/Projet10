from rest_framework import viewsets, permissions
from .models import Issue, Comment
from projects.models import Project
from .serializers import IssueSerializer, CommentSerializer
from .permissions import IsIssueAuthorOrProjectContributor, IsCommentAuthorOrProjectContributor
from rest_framework.exceptions import NotFound


class IssueViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling the creation, retrieval, updating, and deletion of issues.
    
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
        Returns a filtered queryset of issues belonging to a specific project, identified by the URL parameter 'project_pk'.
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
    """
    A viewset for handling the creation, retrieval, updating, and deletion of comments.
    """
    queryset = Comment.objects.select_related('issue', 'issue__project').all()
    serializer_class = CommentSerializer

    # Permissions for authenticated users and custom comment-specific permissions
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthorOrProjectContributor]

    def get_queryset(self):
        """
        Overrides the default queryset to return comments of a specific issue within a project.

        Identified by 'issue_pk' and 'project_pk' in the URL parameters.
        """
        issue_pk = self.kwargs.get('issue_pk')
        project_pk = self.kwargs.get('project_pk')
        if issue_pk and project_pk:
            return self.queryset.filter(issue_id=issue_pk, issue__project_id=project_pk)
        raise NotFound("Project or Issue not found")

    def perform_create(self, serializer):
        """
        Customizes the creation of a Comment instance.

        Sets the comment's author to the current user and associates the comment
        with the issue identified by 'issue_pk' and 'project_pk' in the URL.
        """
        issue = Issue.objects.get(pk=self.kwargs.get('issue_pk'), project_id=self.kwargs.get('project_pk'))
        serializer.save(author=self.request.user, issue=issue)
