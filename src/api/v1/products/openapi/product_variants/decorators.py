from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.authentication.openapi.responses import unauthorized_user_response
from src.api.v1.common.openapi.parameters import jwt_header_parameter
from src.api.v1.common.openapi.responses import (
    bad_request_response,
    forbidden_response,
    not_found_response,
    successful_response,
)
from src.api.v1.products.serializers.product_variants import (
    CreateProductVariantInSerializer,
    GetProductVariantsOutSerializer,
    ProductVariantOutSerializer,
    UpdateProductVariantInSerializer,
)
from src.apps.common.exceptions import NothingToUpdateError
from src.apps.products.exceptions.product_variants import (
    ProductVariantAccessForbiddenError,
    ProductVariantNotFoundError,
    ProductVariantsLimitError,
    ProductVariantsNotFoundError,
)
from src.apps.products.exceptions.products import ProductAccessForbiddenError, ProductNotFoundByIdError
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError


def extend_product_variant_view_schema(view):
    decorator = extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_parameter()],
            request=CreateProductVariantInSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=ProductVariantOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(ProductVariantsLimitError),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    SellerNotFoundError, ProductNotFoundByIdError, UserNotFoundError
                ),
            },
            summary='Create Product Variant POST',
        ),
        get=extend_schema(
            parameters=[jwt_header_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: successful_response(response=GetProductVariantsOutSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    SellerNotFoundError, ProductVariantsNotFoundError, ProductNotFoundByIdError, UserNotFoundError
                ),
            },
            summary='Retrieve Product Variants GET',
        ),
    )
    return decorator(view)


def extend_detail_product_variant_view_schema(view):
    def _update_product_variant_extend_schema(method: str):
        return extend_schema(
            parameters=[jwt_header_parameter()],
            request=UpdateProductVariantInSerializer,
            responses={
                status.HTTP_200_OK: successful_response(response=ProductVariantOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(NothingToUpdateError),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductVariantAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    SellerNotFoundError, ProductVariantNotFoundError, UserNotFoundError
                ),
            },
            summary=f'Update Product Variant {method}',
        )

    decorator = extend_schema_view(
        delete=extend_schema(
            parameters=[jwt_header_parameter()],
            request=None,
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(ProductVariantAccessForbiddenError, UserNotActiveError),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    SellerNotFoundError, ProductVariantNotFoundError, UserNotFoundError
                ),
            },
            summary='Delete Product Variant DELETE',
        ),
        put=_update_product_variant_extend_schema(method='PUT'),
        patch=_update_product_variant_extend_schema(method='PATCH'),
    )
    return decorator(view)
