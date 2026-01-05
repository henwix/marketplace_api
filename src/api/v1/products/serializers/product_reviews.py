from rest_framework import serializers

from src.apps.products.models.product_reviews import ProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'rating', 'text']
        read_only_fields = ['id']
