from rest_framework import serializers

from src.apps.products.models.products import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'uuid',
            'slug',
            'title',
            'description',
            'short_description',
            'is_visible',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['uuid', 'slug']
