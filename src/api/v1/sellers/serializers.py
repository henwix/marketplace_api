from rest_framework import serializers


class SellerInSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False)


class SellerOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(allow_null=True)
    avatar = serializers.CharField(allow_null=True)
    background = serializers.CharField(allow_null=True)
