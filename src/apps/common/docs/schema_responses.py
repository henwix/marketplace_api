from drf_spectacular.utils import OpenApiResponse

from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.common.docs.schema_examples import (
    build_response_example_from_error,
    permission_error_403_response_example,
    unauthorized_error_401_response_example,
)
from src.apps.common.exceptions import ServiceException


def unauthorized_error_401_response() -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Unauthorized error',
        examples=[unauthorized_error_401_response_example()],
    )


def permission_error_403_response() -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Permission error',
        examples=[permission_error_403_response_example()],
    )


def extended_permission_error_403_response(error: ServiceException) -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description='Permission error',
        examples=[
            build_response_example_from_error(error=error),
            permission_error_403_response_example(),
        ],
    )
