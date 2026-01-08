from drf_spectacular.utils import OpenApiResponse, inline_serializer
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import Serializer

from src.api.v1.common.openapi.examples import build_response_example_from_error
from src.api.v1.common.serializers import DetailOutSerializer


def successful_response(*examples, response: type[Serializer]) -> OpenApiResponse:
    return OpenApiResponse(
        response=response,
        description='Successful Response',
        examples=list(examples) if examples else None,
    )


def successful_page_response(response: type[Serializer], paginator: type[PageNumberPagination]) -> OpenApiResponse:
    return OpenApiResponse(
        response=inline_serializer(
            name=f'PaginatedResponse{response.__name__}',
            fields={
                'count': serializers.IntegerField(default=123),
                'next': serializers.URLField(
                    default=f'http://api.example.org/accounts/?{paginator.page_query_param}=4'
                ),
                'previous': serializers.URLField(
                    default=f'http://api.example.org/accounts/?{paginator.page_query_param}=2'
                ),
                'results': response(many=True),
            },
        ),
        description='Successful Response',
    )


def _build_openapi_error_response(*errors: Exception, description: str) -> OpenApiResponse:
    return OpenApiResponse(
        response=DetailOutSerializer,
        description=description,
        examples=[build_response_example_from_error(error=error) for error in errors],
    )


def bad_request_response(*errors: Exception) -> OpenApiResponse:
    return _build_openapi_error_response(*errors, description='Bad Request Error')


def unauthorized_response(*errors: Exception) -> OpenApiResponse:
    return _build_openapi_error_response(*errors, description='Unauthorized Error')


def forbidden_response(*errors: Exception) -> OpenApiResponse:
    return _build_openapi_error_response(*errors, description='Forbidden Error')


def not_found_response(*errors: Exception) -> OpenApiResponse:
    return _build_openapi_error_response(*errors, description='Not Found Error')
