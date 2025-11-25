from drf_spectacular.utils import OpenApiExample

from src.apps.common.exceptions import ServiceException


def build_example_example_from_error(
    error: ServiceException,
    description: str = '',
    summary: str = '',
) -> OpenApiExample:
    return OpenApiExample(
        name=f'{error.message} error',
        value=error.response(),
        response_only=True,
        status_codes=[error.status_code],
        description=description,
        summary=summary,
    )


def detail_response_example(
    name: str,
    value: str,
    status_code: int,
    summary: str = '',
    description: str = '',
) -> OpenApiExample:
    """Return response example with custom 'detail' value."""

    return OpenApiExample(
        name=name,
        value={'detail': value},
        response_only=True,
        status_codes=[status_code],
        summary=summary,
        description=description,
    )
