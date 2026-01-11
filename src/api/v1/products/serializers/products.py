from rest_framework import serializers

from src.api.v1.products.serializers.product_variants import ProductVariantSerializer


class CreateProductInSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(
        allow_blank=True,
        default='',
        required=False,
    )
    short_description = serializers.CharField(
        allow_blank=True,
        default='',
        max_length=500,
        required=False,
    )
    is_visible = serializers.BooleanField(
        default=True,
        required=False,
    )


class UpdateProductInSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(
        allow_blank=True,
        required=False,
    )
    short_description = serializers.CharField(
        allow_blank=True,
        max_length=500,
        required=False,
    )
    is_visible = serializers.BooleanField(required=False)


class ProductOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=300)
    reviews_count = serializers.IntegerField()
    reviews_avg_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    description = serializers.CharField()
    short_description = serializers.CharField(max_length=500)
    is_visible = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class RetrieveProductOutSerializer(ProductOutSerializer):
    seller_url = serializers.HyperlinkedRelatedField(
        view_name='v1:sellers:sellers-detail',
        lookup_field='id',
        lookup_url_kwarg='id',
        source='seller',
        many=False,
        read_only=True,
    )
    variants = ProductVariantSerializer(many=True)


class SearchProductOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='v1:products:products-slug-detail',
        lookup_field='slug',
        lookup_url_kwarg='slug',
        read_only=True,
    )
    is_visible = serializers.BooleanField()
    reviews_count = serializers.IntegerField()
    reviews_avg_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
