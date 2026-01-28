from drf_spectacular.utils import extend_schema, extend_schema_view

from src.api.v1.cart.serializers import AddItemToCartInSerializer


def extend_cart_view_schema(view):
    decorator = extend_schema_view(
        post=extend_schema(
            request=AddItemToCartInSerializer,
            summary='Add Product To Cart POST',
        ),
        get=extend_schema(
            summary='Get Cart GET',
        ),
        delete=extend_schema(
            summary='Delete Product From Cart DELETE',
        ),
    )

    return decorator(view)
