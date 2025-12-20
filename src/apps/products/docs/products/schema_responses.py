from drf_spectacular.utils import OpenApiResponse

from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.common.docs.schema_examples import (
    build_response_example_from_error,
)
from src.apps.products.exceptions.products import (
    ProductAuthorPermissionError,
    ProductNotFoundByIdError,
    ProductNotFoundBySlugError,
)


def product_permission_error_403_response() -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Permission error',
        examples=[
            build_response_example_from_error(ProductAuthorPermissionError),
        ],
    )


def product_not_found_by_id_error_404_response() -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Product not found by id error',
        examples=[
            build_response_example_from_error(ProductNotFoundByIdError),
        ],
    )


def product_not_found_by_slug_error_404_response() -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Product not found by slug error',
        examples=[
            build_response_example_from_error(ProductNotFoundBySlugError),
        ],
    )
