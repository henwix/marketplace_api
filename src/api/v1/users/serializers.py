from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from src.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'avatar', 'password']
        read_only_fields = ['id', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'avatar']
        read_only_fields = ['id', 'avatar']


class PasswordUserSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)

    def validate_new_password(self, value):
        validate_password(value)
        return value
