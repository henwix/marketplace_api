from drf_spectacular.utils import (
    PolymorphicProxySerializer,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers, status

from src.api.v1.authentication.serializers.auth import TokenOutSerializer
from src.api.v1.authentication.serializers.oauth import OAuthVerifyInSerializer
from src.api.v1.common.openapi.parameters import build_enum_query_parameter
from src.api.v1.common.openapi.responses import (
    bad_gateway_response,
    bad_request_response,
    forbidden_response,
    not_found_response,
    successful_response,
    unauthorized_response,
)
from src.api.v1.common.serializers import UrlOutSerializer
from src.apps.authentication.constants import SupportedOAuthProviders
from src.apps.authentication.exceptions.auth_providers import AuthProviderAlreadyConnectedError
from src.apps.authentication.exceptions.oauth import (
    OAuthIncorrectCodeError,
    OAuthIncorrectStateError,
    OAuthInvalidTokenError,
    OAuthNotSupportedProviderError,
    OAuthProviderEmailNotFoundError,
    OAuthProviderRequestError,
    OAuthProviderUidNotFoundError,
    OAuthUnverifiedProviderEmailError,
)
from src.apps.common.exceptions.http_client import HTTPClientError
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
    UserWithDataAlreadyExistsError,
    UserWithEmailAlreadyExistsError,
)


def extend_oauth_get_login_url_view_schema(view):
    decorator = extend_schema_view(
        get=extend_schema(
            parameters=[
                build_enum_query_parameter(
                    name='provider',
                    enum=SupportedOAuthProviders,
                    type=str,
                    required=True,
                )
            ],
            responses={
                status.HTTP_200_OK: successful_response(response=UrlOutSerializer),
                status.HTTP_400_BAD_REQUEST: bad_request_response(OAuthNotSupportedProviderError),
            },
            summary='Get OAuth Login URL GET',
        ),
    )
    return decorator(view)


def extend_oauth_verify_view_schema(view):
    decorator = extend_schema_view(
        post=extend_schema(
            request=OAuthVerifyInSerializer,
            responses={
                status.HTTP_201_CREATED: successful_response(
                    response=PolymorphicProxySerializer(
                        component_name='VerifyOAuthOut',
                        serializers=[
                            TokenOutSerializer,
                            inline_serializer(
                                name='ProviderConnectedSerializer',
                                fields={
                                    'detail': serializers.CharField(
                                        default='Provider successfully connected to your account'
                                    )
                                },
                            ),
                        ],
                        resource_type_field_name=None,
                    )
                ),
                status.HTTP_400_BAD_REQUEST: bad_request_response(
                    OAuthIncorrectStateError,
                    OAuthNotSupportedProviderError,
                    OAuthIncorrectCodeError,
                    OAuthUnverifiedProviderEmailError,
                    OAuthInvalidTokenError,
                    AuthProviderAlreadyConnectedError,
                    UserWithEmailAlreadyExistsError,
                    UserWithDataAlreadyExistsError,
                ),
                status.HTTP_401_UNAUTHORIZED: unauthorized_response(
                    OAuthInvalidTokenError,
                    OAuthProviderEmailNotFoundError,
                    OAuthProviderUidNotFoundError,
                ),
                status.HTTP_403_FORBIDDEN: forbidden_response(
                    UserNotActiveError,
                ),
                status.HTTP_404_NOT_FOUND: not_found_response(
                    UserNotFoundError,
                ),
                status.HTTP_502_BAD_GATEWAY: bad_gateway_response(
                    OAuthProviderRequestError,
                    HTTPClientError,
                ),
            },
            summary='Verify OAuth POST',
        ),
    )
    return decorator(view)
