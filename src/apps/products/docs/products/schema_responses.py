from drf_spectacular.utils import OpenApiResponse

from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.common.docs.schema_examples import (
    build_response_example_from_error,
    permission_error_403_response_example,
)
from src.apps.products.exceptions.products import ProductAuthorPermissionError, ProductNotFoundError


def product_extended_permission_error_403_response() -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Permission error',
        examples=[
            build_response_example_from_error(ProductAuthorPermissionError),
            permission_error_403_response_example(),
        ],
    )


def product_permission_error_403_response() -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Permission error',
        examples=[
            build_response_example_from_error(ProductAuthorPermissionError),
        ],
    )


def product_not_found_error_404_response() -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Product not found error',
        examples=[
            build_response_example_from_error(ProductNotFoundError),
        ],
    )
