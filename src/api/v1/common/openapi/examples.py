from drf_spectacular.utils import OpenApiExample

from src.apps.common.exceptions import ServiceException


def build_response_example_from_error(
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
