from rest_framework import serializers

from src.apps.authentication.constants import SocialAccountProviders


class SocialAccountOutSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=SocialAccountProviders.choices)
    created_at = serializers.DateTimeField()
