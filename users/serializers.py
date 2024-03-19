from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class SignupUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirm', 'age', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_age(self, value):
        """
        Validate that the user is at least 15 years old.
        """
        if value < 15:
            raise serializers.ValidationError("Users must be at least 15 years old.")
        return value

    def validate(self, data):
        """
        Validate that the entered passwords are matching.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        """
        Create a new user instance.
        """
        validated_data.pop('password_confirm', None)  # Remove password_confirm before saving
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for general user operations (read, update, delete).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'can_be_contacted', 'can_data_be_shared', 'created_time']