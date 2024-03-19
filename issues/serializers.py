from rest_framework import serializers
from .models import Issue, Comment, Project, User


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    # Le queryset pour assignee sera défini dans la vue basé sur le projet sélectionné
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
        Initialisation du serializer. Configure le queryset pour l'assignee
        basé sur le projet spécifié dans l'URL.
        """
        super().__init__(*args, **kwargs)

        # Configure le queryset pour 'assignee' en fonction du projet spécifié
        if 'view' in self.context and hasattr(self.context['view'], 'kwargs'):
            project_pk = self.context['view'].kwargs.get('project_pk')
            if project_pk:
                self.fields['assignee'].queryset = User.objects.filter(
                    contributions__project__id=project_pk
                )

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    issue = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'text', 'author', 'created_time']
        read_only_fields = ['author', 'issue']  # issue est toujours en lecture seule