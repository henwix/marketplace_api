import requests
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.api.v1.authentication.serializers import OAuthInSerializer
from src.apps.authentication.use_cases.oauth.get_url import OAuthGitHubGetUrlUseCase
from src.project.containers import resolve_depends


class OAuthGitHubGetUrlView(APIView):
    def get(self, request: Request) -> Response:
        use_case: OAuthGitHubGetUrlUseCase = resolve_depends(OAuthGitHubGetUrlUseCase)
        url = use_case.execute()
        return Response(data={'url': url}, status=status.HTTP_200_OK)


class OAuthGitHubVerifyView(APIView):
    @extend_schema(
        request=OAuthInSerializer,
    )
    def post(self, request: Request) -> Response:
        token_url = 'https://github.com/login/oauth/access_token'
        params = {
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': request.data.get('code'),
        }
        access_token = (
            requests.post(url=token_url, params=params, headers={'Accept': 'application/json'})
            .json()
            .get('access_token')
        )

        user_api_url = 'https://api.github.com/user'
        user_data = requests.get(url=user_api_url, headers={'Authorization': f'Bearer {access_token}'}).json()
        email = user_data.get('email')
        if email is None:
            email_api_url = 'https://api.github.com/user/emails'
            emails = requests.get(url=email_api_url, headers={'Authorization': f'Bearer {access_token}'}).json()
            email = emails[0]
            primary_emails = [e for e in emails if not isinstance(e, dict) or e.get('primary')]
            if primary_emails:
                email = primary_emails[0]
                if isinstance(email, dict):
                    email = email.get('email', '')
        return Response(data={'email': email, 'data': user_data})
