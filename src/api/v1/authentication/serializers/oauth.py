from rest_framework import serializers

from src.api.v1.common.serializers import BaseInSerializer
from src.apps.authentication.constants import SocialAccountProviders


class OAuthProviderInSerializer(BaseInSerializer):
    provider = serializers.ChoiceField(choices=SocialAccountProviders.choices)


class OAuthGetLoginUrlOutSerializer(BaseInSerializer):
    url = serializers.CharField()


class OAuthVerifyInSerializer(BaseInSerializer):
    code = serializers.CharField()
    state = serializers.CharField(min_length=32, max_length=32)
    provider = serializers.ChoiceField(choices=SocialAccountProviders.choices)
