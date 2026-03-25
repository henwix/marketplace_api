from drf_spectacular.utils import OpenApiResponse, PolymorphicProxySerializer

from src.api.v1.authentication.openapi.auth.examples import (
    unauthorized_token_expired_response_example,
    unauthorized_token_invalid_response_example,
)
from src.api.v1.authentication.serializers.auth import DetailTokenOutSerializer
from src.api.v1.common.openapi.examples import (
    build_response_example_from_error,
)
from src.api.v1.common.serializers import DetailOutSerializer
from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError


def unauthorized_user_response(include_credentials_error: bool = True) -> OpenApiResponse:
    response = OpenApiResponse(
        response=PolymorphicProxySerializer(
            component_name='Unauthorized response',
            serializers=[DetailTokenOutSerializer, DetailOutSerializer],
            resource_type_field_name=None,
        )
        if include_credentials_error is True
        else DetailTokenOutSerializer,
        description='Unauthorized Error',
        examples=[
            unauthorized_token_invalid_response_example(),
            unauthorized_token_expired_response_example(),
        ],
    )

    if include_credentials_error is True:
        response.examples.append(build_response_example_from_error(error=AuthCredentialsNotProvidedError))
    return response
