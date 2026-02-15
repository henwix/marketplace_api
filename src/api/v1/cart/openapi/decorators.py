from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.cart.serializers import AddItemToCartInSerializer, CartItemOutSerializer


def extend_cart_view_schema(view):
    decorator = extend_schema_view(
        post=extend_schema(
            request=AddItemToCartInSerializer,
            responses={
                status.HTTP_201_CREATED: CartItemOutSerializer,
            },
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
