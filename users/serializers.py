from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for general user operations (read, update, delete).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'can_be_contacted', 'can_data_be_shared', 'created_time']

class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'age', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(RegisterUserSerializer, self).create(validated_data)

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError("Users must be at least 15 years old.")
        return value