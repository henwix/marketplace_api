from drf_spectacular.utils import extend_schema

from src.api.v1.products.serializers.product_variants import ProductVariantSerializer

extend_create_product_variant_schema = extend_schema(
    request=ProductVariantSerializer, responses=ProductVariantSerializer, summary='Create Product Variant POST'
)
