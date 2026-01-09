from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from src.apps.users.validators import user_phone_validator


class CreateUserInSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    phone = serializers.CharField(max_length=20, validators=[user_phone_validator])
    password = serializers.CharField(validators=[validate_password])


class UpdateUserInSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    phone = serializers.CharField(max_length=20, validators=[user_phone_validator])


class SetPasswordUserInSerializer(serializers.Serializer):
    new_password = serializers.CharField(validators=[validate_password])


class PreviewUserOutSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    avatar = serializers.CharField(allow_null=True)


class UserOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    phone = serializers.CharField(max_length=20, validators=[user_phone_validator])
    avatar = serializers.CharField(allow_null=True)
