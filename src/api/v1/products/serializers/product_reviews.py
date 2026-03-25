from rest_framework import serializers

from src.api.v1.common.serializers import BaseInSerializer
from src.api.v1.users.serializers import PreviewUserOutSerializer


class CreateProductReviewInSerializer(BaseInSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5, default=1)
    text = serializers.CharField()


class UpdateProductReviewInSerializer(BaseInSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField()


class ProductReviewOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField()


class RetrieveProductReviewOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    user = PreviewUserOutSerializer()
