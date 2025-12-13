from drf_spectacular.utils import extend_schema, extend_schema_view

from src.api.v1.products.serializers.products import ProductSerializer, RetrieveProductSerializer

extend_create_product_view_schema = extend_schema_view(
    post=extend_schema(request=ProductSerializer, responses=ProductSerializer, summary='Create Product POST')
)


extend_get_product_by_slug_view_schema = extend_schema_view(
    get=extend_schema(request=None, responses=RetrieveProductSerializer, summary='Retrieve Product By Slug GET')
)


extend_detail_product_view_schema = extend_schema_view(
    get=extend_schema(request=None, responses=RetrieveProductSerializer, summary='Retrieve Product By Id GET'),
    delete=extend_schema(request=None, responses={204: None}, summary='Delete Product DELETE'),
    put=extend_schema(request=ProductSerializer, responses=ProductSerializer, summary='Update Product PUT'),
    patch=extend_schema(request=ProductSerializer, responses=ProductSerializer, summary='Update Product PATCH'),
)
