from rest_framework import viewsets, permissions
from .models import Issue, Comment
from .serializers import IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsContributorOrReadOnly


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        context = super(IssueViewSet, self).get_serializer_context()
        context.update({'request': self.request})
        return context


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)