from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.products.serializers.product_variants import GetProductVariantsOutSerializer, ProductVariantSerializer
from src.apps.common.docs.schema_parameters import jwt_header_request_parameter
from src.apps.common.docs.schema_responses import (
    bad_request_error_response,
    forbidden_error_response,
    not_found_error_response,
    successful_response,
)
from src.apps.products.exceptions.product_variants import (
    ProductVariantAccessForbiddenError,
    ProductVariantNotFoundError,
    ProductVariantsLimitError,
    ProductVariantsNotFoundError,
)
from src.apps.products.exceptions.products import ProductAccessForbiddenError, ProductNotFoundByIdError
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.users.docs.schema_responses import (
    unauthorized_user_response,
)


def extend_product_variant_view_schema():
    return extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=ProductVariantSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(response=ProductVariantSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_error_response(ProductVariantsLimitError),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_error_response(ProductAccessForbiddenError),
                status.HTTP_404_NOT_FOUND: not_found_error_response(SellerNotFoundError, ProductNotFoundByIdError),
            },
            summary='Create Product Variant POST',
        ),
        get=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: successful_response(response=GetProductVariantsOutSerializer),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_error_response(ProductAccessForbiddenError),
                status.HTTP_404_NOT_FOUND: not_found_error_response(
                    SellerNotFoundError, ProductVariantsNotFoundError, ProductNotFoundByIdError
                ),
            },
            summary='Retrieve Product Variants GET',
        ),
    )


def _update_product_variant_extend_schema(method: str):
    return extend_schema(
        parameters=[jwt_header_request_parameter()],
        request=ProductVariantSerializer,
        responses={
            status.HTTP_200_OK: successful_response(response=ProductVariantSerializer),
            status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
            status.HTTP_403_FORBIDDEN: forbidden_error_response(ProductVariantAccessForbiddenError),
            status.HTTP_404_NOT_FOUND: not_found_error_response(SellerNotFoundError, ProductVariantNotFoundError),
        },
        summary=f'Update Product Variant {method}',
    )


def extend_detail_product_variant_view_schema():
    return extend_schema_view(
        delete=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_error_response(ProductVariantAccessForbiddenError),
                status.HTTP_404_NOT_FOUND: not_found_error_response(SellerNotFoundError, ProductVariantNotFoundError),
            },
            summary='Delete Product Variant DELETE',
        ),
        put=_update_product_variant_extend_schema(method='PUT'),
        patch=_update_product_variant_extend_schema(method='PATCH'),
    )
