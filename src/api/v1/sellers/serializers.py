from rest_framework import serializers


class CreateSellerInSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True, default='')


class UpdateSellerInSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_blank=True)


class SellerOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    avatar = serializers.CharField(allow_null=True)
    background = serializers.CharField(allow_null=True)
