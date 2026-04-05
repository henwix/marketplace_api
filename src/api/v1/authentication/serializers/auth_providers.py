from rest_framework import serializers

from src.api.v1.common.serializers import BaseInSerializer
from src.apps.authentication.constants import SupportedAuthProviders


class AuthProviderInSerializer(BaseInSerializer):
    provider = serializers.ChoiceField(choices=SupportedAuthProviders.choices)


class AuthProviderOutSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=SupportedAuthProviders.choices)
    created_at = serializers.DateTimeField()
