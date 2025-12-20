from enum import Enum
from typing import Any

from django.db import models
from drf_spectacular.utils import OpenApiParameter


def jwt_header_request_parameter() -> OpenApiParameter:
    return OpenApiParameter(
        name='Authorization',
        type=str,
        location=OpenApiParameter.HEADER,
        required=False,
        description='JWT access token: Bearer <token>',
    )


def build_enum_query_param(
    name: str,
    enum: type[models.TextChoices] | type[Enum],
    type: Any = str,
    description: str = '',
    required: bool = False,
) -> OpenApiParameter:
    """Build query parameter with detailed description based on provided
    Enum."""

    desc_list = '\n'.join([f'- `{i.value}` — {i.label}' for i in enum])

    return OpenApiParameter(
        name=name,
        location=OpenApiParameter.QUERY,
        required=required,
        type=type,
        enum=enum,
        description=f'{description}\n\n{desc_list}',
    )
