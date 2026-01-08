from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from src.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'avatar', 'password']
        read_only_fields = ['id', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        validate_password(value)
        return value


class PreviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'avatar']
        read_only_fields = ['id', 'avatar']


class PasswordUserSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, help_text=_('New password for the user'))

    def validate_new_password(self, value):
        validate_password(value)
        return value
