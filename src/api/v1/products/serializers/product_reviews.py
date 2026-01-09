from rest_framework import serializers

from src.api.v1.users.serializers import PreviewUserOutSerializer
from src.apps.products.models.product_reviews import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'rating', 'text']
        read_only_fields = ['id']


class RetrieveProductReviewSerializer(serializers.ModelSerializer):
    user = PreviewUserOutSerializer()

    class Meta:
        model = ProductReview
        fields = ['id', 'rating', 'text', 'created_at', 'updated_at', 'user']
