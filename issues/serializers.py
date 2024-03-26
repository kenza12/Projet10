from rest_framework import serializers
from .models import Issue, Comment, Project, User


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for the Issue model.
    """
    author = serializers.ReadOnlyField(source='author.username')
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    # Define a field for assignee, setting an initial empty queryset
    # The queryset will be dynamically set based on the selected project
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(), 
        required=False, 
        allow_null=True
    )

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'project', 'tag', 'status', 
                  'priority', 'assignee', 'author', 'created_time']
        read_only_fields = ['author', 'project']

    def __init__(self, *args, **kwargs):
        """
        Overrides the default initialization to dynamically set the queryset for the 'assignee' field.
        
        The queryset for the 'assignee' field is determined based on the project to which the issue belongs.
        This ensures that only users who are contributors to the relevant project can be assigned.
        """
        super().__init__(*args, **kwargs)

        # Set the queryset for 'assignee' dynamically based on the project specified in the URL
        if 'view' in self.context and hasattr(self.context['view'], 'kwargs'):
            project_pk = self.context['view'].kwargs.get('project_pk')
            if project_pk:
                # Filter users who are contributors to the specific project
                self.fields['assignee'].queryset = User.objects.filter(
                    contributions__project__id=project_pk
                )

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    author = serializers.ReadOnlyField(source='author.username')
    issue = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'text', 'author', 'created_time']
        read_only_fields = ['author', 'issue']