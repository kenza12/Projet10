from rest_framework import serializers
from .models import Project, Contributor
from users.models import User


class ContributorCreateSerializer(serializers.ModelSerializer):
    """
    This serializer is responsible for validating and saving a new contributor to a project,
    with the ability to select a user from all available users in the User model.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ['user']

    def create(self, validated_data):
        """
        Create a new contributor instance.

        Args:
            validated_data (dict): Validated data for creating a contributor.

        Returns:
            Contributor: A new contributor instance.
        """
        user = validated_data['user']
        project = self.context['project']
        return Contributor.objects.create(project=project, user=user)


class ContributorListSerializer(serializers.ModelSerializer):
    """
    Serializer to list contributors with detailed information.
    """
    # Read-only fields to display username and project title
    username = serializers.ReadOnlyField(source='user.username')
    project_title = serializers.ReadOnlyField(source='project.title')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'username', 'project', 'project_title', 'date_joined']


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing projects.
    """
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['author'] # Author field is read-only


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed view of a project, including its contributors.
    """
    # Nested serializer to include project contributors
    contributors = ContributorListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time', 'contributors']
