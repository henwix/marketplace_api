from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.v1.authentication.openapi.oauth.decorators import (
    extend_oauth_get_login_url_view_schema,
    extend_oauth_verify_view_schema,
)
from src.api.v1.authentication.serializers.oauth import OAuthGetLoginUrlInSerializer, OAuthVerifyInSerializer
from src.apps.authentication.commands.oauth import OAuthGetLoginUrlCommand, OAuthVerifyCommand
from src.apps.authentication.use_cases.oauth.get_url import OAuthGetLoginUrlUseCase
from src.apps.authentication.use_cases.oauth.verify_code import OAuthVerifyUseCase
from src.project.containers import resolve_depends


@extend_oauth_get_login_url_view_schema
class OAuthGetLoginUrlView(APIView):
    def get(self, request: Request) -> Response:
        request_data = OAuthGetLoginUrlInSerializer.validate_data(data=request.query_params)
        use_case: OAuthGetLoginUrlUseCase = resolve_depends(OAuthGetLoginUrlUseCase)
        command = OAuthGetLoginUrlCommand(**request_data)
        url = use_case.execute(command=command)
        return Response(data={'url': url}, status=status.HTTP_200_OK)


@extend_oauth_verify_view_schema
class OAuthVerifyView(APIView):
    def post(self, request: Request) -> Response:
        request_data = OAuthVerifyInSerializer.validate_data(data=request.data)
        use_case: OAuthVerifyUseCase = resolve_depends(OAuthVerifyUseCase)
        command = OAuthVerifyCommand(user_id=request.user.id, **request_data)
        result = use_case.execute(command=command)
        return Response(data=result, status=status.HTTP_201_CREATED)
