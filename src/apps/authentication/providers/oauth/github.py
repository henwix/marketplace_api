from dataclasses import dataclass
from urllib.parse import urlencode

from django.conf import settings

from src.apps.authentication.constants import SocialAccountProviders
from src.apps.authentication.exceptions.oauth import (
    OAuthIncorrectCodeError,
    OAuthProviderEmailNotFoundError,
    OAuthProviderRequestError,
    OAuthUnverifiedProviderEmailError,
)
from src.apps.authentication.providers.oauth.base import BaseOAuthProvider
from src.apps.common.clients.http_client import BaseHTTPClient


@dataclass(eq=False)
class OAuthGitHubProvider(BaseOAuthProvider):
    _OAUTH_URL = 'https://github.com/login/oauth'
    _USER_API_URL = 'https://api.github.com/user'
    _CLIENT_ID = settings.GITHUB_CLIENT_ID
    _CLIENT_SECRET = settings.GITHUB_CLIENT_SECRET
    _REDIRECT_URI = settings.GITHUB_REDIRECT_URI
    _SCOPE = 'read:user user:email'

    http_client: BaseHTTPClient

    def _get_user_names(self, name: str) -> tuple[str, str]:
        try:
            first_name, last_name = name.split(' ', 1)
        except ValueError:
            first_name = name
            last_name = name

        return first_name.strip(), last_name.strip()

    @property
    def provider_name(self) -> str:
        return SocialAccountProviders.GITHUB

    def exchange_code(self, code: str) -> str:
        request_body = {
            'client_id': self._CLIENT_ID,
            'client_secret': self._CLIENT_SECRET,
            'code': code,
        }
        headers = {
            'Accept': 'application/json',
        }
        response = self.http_client.post(
            url=f'{self._OAUTH_URL}/access_token',
            data=request_body,
            headers=headers,
        )

        error = response.get('error', None)

        if error is not None:
            if error == 'bad_verification_code':
                raise OAuthIncorrectCodeError(code=code)
            elif error == 'unverified_user_email':
                raise OAuthUnverifiedProviderEmailError()
            else:
                raise OAuthProviderRequestError(error=error, code=code)

        if 'access_token' not in response:
            raise OAuthProviderRequestError(error='invalid_oauth_response', code=code)

        return response['access_token']

    def get_user_data(self, token: str) -> dict[str, str]:
        headers = {
            'Authorization': f'Bearer {token}',
        }
        response = self.http_client.get(url=self._USER_API_URL, headers=headers)

        if response.get('email', None) is None:
            emails = self.http_client.get(url=f'{self._USER_API_URL}/emails', headers=headers)
            primary_emails = [e for e in emails if e.get('primary') and e.get('verified')]
            if not primary_emails:
                raise OAuthProviderEmailNotFoundError()
            response['email'] = primary_emails[0].get('email') if primary_emails else emails[0].get('email')

        first_name, last_name = self._get_user_names(name=response.get('name') or response.get('login'))
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': response.get('email'),
            'provider_uid': response.get('id'),
            'avatar': response.get('avatar_url'),
        }
        return user_data

    def get_login_url(self, state: str) -> str:
        params = {
            'client_id': self._CLIENT_ID,
            'redirect_url': self._REDIRECT_URI,
            'scope': self._SCOPE,
            'state': state,
        }
        return f'{self._OAUTH_URL}/authorize?{urlencode(query=params)}'
