from rest_framework import serializers
from .models import Issue, Comment, Project, User


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.none(),  # Sera remplacé dans la view
        required=True
    )
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(),  # Sera remplacé dans la view
        required=False,
        allow_null=True
    )

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'tag', 'status', 'priority', 'assignee', 'author', 'created_time']
        read_only_fields = ['author']

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(
            contributors__user=user
        )
        self.fields['assignee'].queryset = User.objects.filter(
            contributions__project__contributors__user=user
        )

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'text', 'author', 'created_time']
        read_only_fields = ['author']