from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.authentication.openapi.responses import unauthorized_user_response
from src.api.v1.cart.serializers import AddItemToCartInSerializer, CartItemOutSerializer
from src.api.v1.common.openapi.parameters import jwt_header_parameter
from src.api.v1.common.openapi.responses import (
    bad_request_response,
    forbidden_response,
    not_found_response,
    successful_response,
)
from src.apps.cart.exceptions import ItemAlreadyInCartError, ItemProductVariantOrSellerNotFoundError
from src.apps.products.exceptions.product_variants import (
    ProductVariantAccessForbiddenError,
    ProductVariantNotFoundError,
    ProductVariantOutOfStockError,
    QuantityGreaterThanStockError,
)
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError


def extend_cart_view_schema(view):
    decorator = extend_schema_view(
        post=extend_schema(
            request=AddItemToCartInSerializer,
            parameters=[jwt_header_parameter()],
            responses={
                status.HTTP_201_CREATED: successful_response(response=CartItemOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(
                    ItemAlreadyInCartError,
                    ProductVariantOutOfStockError,
                    QuantityGreaterThanStockError,
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(
                    UserNotActiveError,
                    ProductVariantAccessForbiddenError,
                ),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                    ProductVariantNotFoundError,
                    ItemProductVariantOrSellerNotFoundError,
                ),
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
