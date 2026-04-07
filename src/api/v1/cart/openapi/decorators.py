from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.authentication.openapi.auth.responses import unauthorized_user_response
from src.api.v1.cart.serializers import AddCartItemInSerializer, CartItemOutSerializer, GetCartItemsOutSerializer
from src.api.v1.common.openapi.parameters import jwt_header_parameter, query_parameter
from src.api.v1.common.openapi.responses import (
    bad_request_response,
    forbidden_response,
    not_found_response,
    successful_response,
)
from src.apps.cart.exceptions import (
    CartEmptyError,
    CartLimitError,
    ItemAlreadyInCartError,
    ItemNotFoundInCartError,
    ItemProductVariantOrSellerNotFoundError,
)
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
            request=AddCartItemInSerializer,
            parameters=[jwt_header_parameter()],
            responses={
                status.HTTP_201_CREATED: successful_response(response=CartItemOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(
                    ItemAlreadyInCartError,
                    CartLimitError,
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
            summary='Add Cart Item POST',
        ),
        get=extend_schema(
            request=None,
            parameters=[jwt_header_parameter()],
            responses={
                status.HTTP_200_OK: successful_response(response=GetCartItemsOutSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(
                    UserNotActiveError,
                ),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                    CartEmptyError,
                ),
            },
            summary='Get Cart GET',
        ),
        delete=extend_schema(
            parameters=[
                jwt_header_parameter(),
                query_parameter(name='product_variant_id', type=UUID, required=True),
            ],
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(
                    UserNotActiveError,
                ),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                    ItemNotFoundInCartError,
                ),
            },
            summary='Delete Cart Item DELETE',
        ),
    )

    return decorator(view)


def extend_clear_cart_view_schema(view):
    decorator = extend_schema_view(
        delete=extend_schema(
            parameters=[jwt_header_parameter()],
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: bad_request_response(UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                    CartEmptyError,
                ),
            },
            summary='Clear Cart DELETE',
        )
    )
    return decorator(view)
