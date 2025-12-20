from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.common.serializers import DetailOutSerializer
from src.api.v1.products.serializers.product_variants import GetProductVariantsOutSerializer, ProductVariantSerializer
from src.apps.common.docs.schema_examples import build_response_example_from_error
from src.apps.common.docs.schema_parameters import jwt_header_request_parameter
from src.apps.common.docs.schema_responses import (
    extended_permission_error_403_response,
    unauthorized_error_401_response,
)
from src.apps.products.docs.product_variants.schema_responses import product_variant_not_found_error_404_response
from src.apps.products.docs.products.schema_responses import (
    product_not_found_by_id_error_404_response,
)
from src.apps.products.exceptions.product_variants import (
    ProductVariantAuthorPermissionError,
    ProductVariantsLimitError,
    ProductVariantsNotFoundError,
)
from src.apps.products.exceptions.products import ProductAuthorPermissionError, ProductNotFoundByIdError


def extend_product_variant_view_schema():
    return extend_schema_view(
        post=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=ProductVariantSerializer,
            responses={
                status.HTTP_201_CREATED: OpenApiResponse(
                    response=ProductVariantSerializer,
                    description='Product variant has been created',
                ),
                status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                    response=DetailOutSerializer,
                    description='Product variants limit error',
                    examples=[
                        build_response_example_from_error(ProductVariantsLimitError),
                    ],
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
                status.HTTP_403_FORBIDDEN: extended_permission_error_403_response(error=ProductAuthorPermissionError),
                status.HTTP_404_NOT_FOUND: product_not_found_by_id_error_404_response(),
            },
            summary='Create Product Variant POST',
        ),
        get=extend_schema(
            parameters=[jwt_header_request_parameter()],
            request=None,
            responses={
                status.HTTP_200_OK: OpenApiResponse(
                    response=GetProductVariantsOutSerializer,
                    description='Product variants have been retrieved',
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
                status.HTTP_403_FORBIDDEN: extended_permission_error_403_response(error=ProductAuthorPermissionError),
                status.HTTP_404_NOT_FOUND: OpenApiResponse(
                    response=DetailOutSerializer,
                    description='Product not found by id or product variants not found error',
                    examples=[
                        build_response_example_from_error(ProductNotFoundByIdError),
                        build_response_example_from_error(ProductVariantsNotFoundError),
                    ],
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
            status.HTTP_200_OK: OpenApiResponse(
                response=ProductVariantSerializer,
                description='Product variant has been updated',
            ),
            status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
            status.HTTP_403_FORBIDDEN: extended_permission_error_403_response(
                error=ProductVariantAuthorPermissionError
            ),
            status.HTTP_404_NOT_FOUND: product_variant_not_found_error_404_response(),
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
                status.HTTP_401_UNAUTHORIZED: unauthorized_error_401_response(),
                status.HTTP_403_FORBIDDEN: extended_permission_error_403_response(
                    error=ProductVariantAuthorPermissionError
                ),
                status.HTTP_404_NOT_FOUND: product_variant_not_found_error_404_response(),
            },
            summary='Delete Product Variant DELETE',
        ),
        put=_update_product_variant_extend_schema(method='PUT'),
        patch=_update_product_variant_extend_schema(method='PATCH'),
    )
