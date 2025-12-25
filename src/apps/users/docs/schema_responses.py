from drf_spectacular.utils import OpenApiResponse

from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.common.docs.schema_examples import (
    build_response_example_from_error,
)
from src.apps.users.docs.schema_examples import (
    unauthorized_token_expired_error_401_response_example,
    unauthorized_token_invalid_error_401_response_example,
)
from src.apps.users.exceptions.users import (
    UserAuthCredentialsNotProvidedError,
    UserAuthNotActiveError,
    UserAuthNotFoundError,
)


def unauthorized_user_response(include_credentials_error: bool = True) -> OpenApiResponse:
    response = OpenApiResponse(
        response=DetailOutSerializer,
        description='Unauthorized Error',
        examples=[
            build_response_example_from_error(error=UserAuthNotFoundError),
            build_response_example_from_error(error=UserAuthNotActiveError),
            unauthorized_token_invalid_error_401_response_example(),
            unauthorized_token_expired_error_401_response_example(),
        ],
    )

    if include_credentials_error is True:
        response.examples.append(build_response_example_from_error(error=UserAuthCredentialsNotProvidedError))
    return response
