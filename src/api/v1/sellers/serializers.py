from rest_framework import serializers

from src.api.v1.common.serializers import BaseInSerializer


class CreateSellerInSerializer(BaseInSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, default='')


class UpdateSellerInSerializer(BaseInSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True)


class SellerOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    avatar = serializers.CharField(allow_null=True)
    background = serializers.CharField(allow_null=True)
