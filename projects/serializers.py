from rest_framework import serializers
from .models import Project, Contributor
from django.contrib.auth import get_user_model


User = get_user_model()


class ContributorCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ['user']

    def create(self, validated_data):
        project = self.context['project']
        user = validated_data['user']
        return Contributor.objects.create(project=project, user=user)

class ContributorCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Contributor
        fields = ['user']
        extra_kwargs = {
            'user': {'write_only': True},
        }

    def create(self, validated_data):
        project = self.context['project']
        user = validated_data['user']
        return Contributor.objects.create(project=project, user=user)

class ContributorListSerializer(serializers.ModelSerializer):
    """
    Serializer pour lister les contributeurs avec des informations détaillées.
    """
    username = serializers.ReadOnlyField(source='user.username')
    project_title = serializers.ReadOnlyField(source='project.title')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'username', 'project', 'project_title', 'date_joined']

class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer pour la liste des projets.
    """
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['author']

class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer pour les détails d'un projet, incluant les contributeurs.
    """
    contributors = ContributorListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time', 'contributors']
