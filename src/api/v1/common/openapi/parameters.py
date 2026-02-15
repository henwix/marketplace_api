from enum import Enum
from typing import Any

from django.db import models
from drf_spectacular.utils import OpenApiParameter
from rest_framework.pagination import BasePagination, CursorPagination, PageNumberPagination
from rest_framework.settings import api_settings


def jwt_header_parameter() -> OpenApiParameter:
    return OpenApiParameter(
        name='Authorization',
        type=str,
        location=OpenApiParameter.HEADER,
        required=False,
        description='JWT access token: Bearer <token>',
    )


def search_query_parameter() -> OpenApiParameter:
    return query_parameter(
        name=api_settings.SEARCH_PARAM,
        description='A search term',
    )


def ordering_query_parameter(enum: type[Enum]) -> OpenApiParameter:
    return build_enum_query_parameter(
        name=api_settings.ORDERING_PARAM,
        enum=enum,
        description='Which field to use when ordering the results',
    )


def cursor_query_parameter(paginator: type[CursorPagination]) -> OpenApiParameter:
    return query_parameter(
        name=paginator.cursor_query_param,
        type=str,
        description='The pagination cursor value',
    )


def page_query_parameter(paginator: type[PageNumberPagination]) -> OpenApiParameter:
    return query_parameter(
        name=paginator.page_query_param,
        type=int,
        description='A page number within the paginated result set',
    )


def page_size_query_parameter(paginator: type[BasePagination]) -> OpenApiParameter:
    return query_parameter(
        name=paginator.page_size_query_param,
        type=int,
        description='Number of results to return per page',
    )


def query_parameter(
    name: str,
    type: Any = str,
    description: str = '',
    required: bool = False,
) -> OpenApiParameter:
    """Build query parameter"""

    return OpenApiParameter(
        name=name,
        location=OpenApiParameter.QUERY,
        required=required,
        type=type,
        description=description,
    )


def build_enum_query_parameter(
    name: str,
    enum: type[models.TextChoices] | type[Enum],
    type: Any = str,
    description: str = '',
    required: bool = False,
) -> OpenApiParameter:
    """Build query parameter with detailed description based on provided Enum"""

    desc_list = '\n'.join([f'- `{i.value}` — {i.label}' for i in enum])

    return OpenApiParameter(
        name=name,
        location=OpenApiParameter.QUERY,
        required=required,
        type=type,
        enum=enum,
        description=f'{description}\n\n{desc_list}',
    )
