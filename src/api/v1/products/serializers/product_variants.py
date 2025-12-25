from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from src.apps.products.models.product_variants import ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'title', 'price', 'stock', 'is_visible', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class GetProductVariantsOutSerializer(serializers.Serializer):
    count = serializers.IntegerField(help_text=_('Product variants count'))
    results = ProductVariantSerializer(many=True, help_text=_('Product variants'))
