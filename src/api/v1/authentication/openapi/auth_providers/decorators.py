from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status

from src.api.v1.authentication.openapi.auth.responses import unauthorized_user_response
from src.api.v1.authentication.serializers.auth_providers import AuthProviderOutSerializer
from src.api.v1.common.openapi.parameters import build_enum_query_parameter
from src.api.v1.common.openapi.responses import (
    bad_request_response,
    forbidden_response,
    not_found_response,
    successful_response,
)
from src.apps.authentication.constants import SupportedAuthProviders
from src.apps.authentication.exceptions.auth_providers import (
    AuthProviderNotConnectedError,
    AuthProviderNotSupportedError,
    AuthProvidersNotConnectedError,
    UnableToDisconnectAuthProviderError,
)
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError


def extend_auth_provider_view_schema(view):
    decorator = extend_schema_view(
        get=extend_schema(
            responses={
                status.HTTP_200_OK: successful_response(
                    response=AuthProviderOutSerializer(many=True),
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(
                    UserNotActiveError,
                ),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                ),
            },
            summary='Get Connected Auth Providers GET',
        ),
        delete=extend_schema(
            parameters=[
                build_enum_query_parameter(
                    name='provider',
                    enum=SupportedAuthProviders,
                    type=str,
                    required=True,
                )
            ],
            responses={
                status.HTTP_204_NO_CONTENT: None,
                status.HTTP_400_BAD_REQUEST: bad_request_response(
                    AuthProviderNotSupportedError,
                    UnableToDisconnectAuthProviderError,
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_user_response(),
                status.HTTP_403_FORBIDDEN: forbidden_response(
                    UserNotActiveError,
                ),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                    AuthProvidersNotConnectedError,
                    AuthProviderNotConnectedError,
                ),
            },
            summary='Disconnect Auth Provider DELETE',
        ),
    )
    return decorator(view)
