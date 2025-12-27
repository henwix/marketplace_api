from drf_spectacular.utils import OpenApiResponse
from rest_framework.serializers import Serializer

from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.common.docs.schema_examples import (
    build_response_example_from_error,
    permission_error_403_response_example,
    unauthorized_error_401_response_example,
)


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


def _build_openapi_response(*errors: Exception, description: str) -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description=description,
        examples=[build_response_example_from_error(error=error) for error in errors],
    )


def successful_response(*examples, response: Serializer) -> OpenApiResponse:
    return OpenApiResponse(
        response=response,
        description='Successful Response',
        examples=list(examples) if examples else None,
    )


def bad_request_response(*errors: Exception) -> OpenApiResponse:
    return _build_openapi_response(*errors, description='Bad Request Error')


def unauthorized_response(*errors: Exception) -> OpenApiResponse:
    return _build_openapi_response(*errors, description='Unauthorized Error')


def forbidden_response(*errors: Exception) -> OpenApiResponse:
    return _build_openapi_response(*errors, description='Forbidden Error')


def not_found_response(*errors: Exception) -> OpenApiResponse:
    return _build_openapi_response(*errors, description='Not Found Error')
