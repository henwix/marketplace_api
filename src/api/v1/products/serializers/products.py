from rest_framework import serializers

from src.api.v1.products.serializers.product_variants import ProductVariantSerializer
from src.apps.products.models.products import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'short_description',
            'is_visible',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug']


class RetrieveProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    seller_url = serializers.HyperlinkedRelatedField(
        view_name='v1:sellers:sellers-detail',
        lookup_field='id',
        lookup_url_kwarg='id',
        source='seller',
        many=False,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'seller_url',
            'description',
            'short_description',
            'is_visible',
            'created_at',
            'updated_at',
            'variants',
        ]


class SearchProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='v1:products:products-slug',
        lookup_field='slug',
        lookup_url_kwarg='slug',
        read_only=True,
    )
    variants_count = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'url', 'title', 'is_visible', 'variants_count', 'price']
