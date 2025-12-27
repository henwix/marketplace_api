from drf_spectacular.utils import OpenApiResponse

from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.authentication.docs.schema_examples import (
    unauthorized_token_expired_response_example,
    unauthorized_token_invalid_response_example,
)
from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.common.docs.schema_examples import (
    build_response_example_from_error,
)


def unauthorized_user_response(include_credentials_error: bool = True) -> OpenApiResponse:
    response = OpenApiResponse(
        response=DetailOutSerializer,
        description='Unauthorized Error',
        examples=[
            unauthorized_token_invalid_response_example(),
            unauthorized_token_expired_response_example(),
        ],
    )

    if include_credentials_error is True:
        response.examples.append(build_response_example_from_error(error=AuthCredentialsNotProvidedError))
    return response
