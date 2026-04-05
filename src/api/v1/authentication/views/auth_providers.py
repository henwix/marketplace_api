from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.v1.authentication.openapi.auth_providers.decorators import extend_auth_provider_view_schema
from src.api.v1.authentication.serializers.auth_providers import AuthProviderInSerializer, AuthProviderOutSerializer
from src.apps.authentication.commands.auth_providers import (
    DisconnectAuthProviderCommand,
    GetConnectedAuthProvidersCommand,
)
from src.apps.authentication.use_cases.auth_providers.disconnect_provider import DisconnectAuthProviderUseCase
from src.apps.authentication.use_cases.auth_providers.get_connected_providers import GetConnectedAuthProvidersUseCase
from src.project.containers import resolve_depends


@extend_auth_provider_view_schema
class AuthProviderView(APIView):
    def get(self, request: Request) -> Response:
        use_case: GetConnectedAuthProvidersUseCase = resolve_depends(GetConnectedAuthProvidersUseCase)
        command = GetConnectedAuthProvidersCommand(user_id=request.user.id)
        providers = use_case.execute(command=command)
        return Response(data=AuthProviderOutSerializer(providers, many=True).data, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        request_data = AuthProviderInSerializer.validate_data(data=request.query_params)
        use_case: DisconnectAuthProviderUseCase = resolve_depends(DisconnectAuthProviderUseCase)
        command = DisconnectAuthProviderCommand(user_id=request.user.id, **request_data)
        use_case.execute(command=command)
        return Response(status=status.HTTP_204_NO_CONTENT)
