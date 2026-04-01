from dataclasses import dataclass
from urllib.parse import unquote, urlencode
from uuid import uuid4

from django.conf import settings
from requests import HTTPError, Response

from src.apps.authentication.constants import SocialAccountProviders
from src.apps.authentication.exceptions.oauth import (
    OAuthIncorrectCodeError,
    OAuthProviderEmailNotFoundError,
    OAuthProviderRequestError,
    OAuthProviderUidNotFoundError,
)
from src.apps.authentication.providers.oauth.base import BaseOAuthProvider
from src.apps.authentication.services.jwt import BaseJWTService
from src.apps.common.clients.http_client import BaseHTTPClient
from src.apps.common.exceptions.http_client import HTTPClientError


@dataclass(eq=False)
class OAuthGoogleProvider(BaseOAuthProvider):
    http_client: BaseHTTPClient
    jwt_service: BaseJWTService

    def __post_init__(self):
        self._OAUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
        self._TOKEN_URL = 'https://oauth2.googleapis.com/token'
        self._CLIENT_ID = settings.OAUTH_GOOGLE_CLIENT_ID
        self._CLIENT_SECRET = settings.OAUTH_GOOGLE_CLIENT_SECRET
        self._REDIRECT_URI = settings.OAUTH_GOOGLE_REDIRECT_URI
        self._SCOPE = 'openid profile email'
        self._GRANT_TYPE = 'authorization_code'
        self._RESPONSE_TYPE = 'code'
        self._ACCESS_TYPE = 'offline'

    def _get_user_names(
        self,
        given_name: str | None,
        family_name: str | None,
        fullname: str | None,
    ) -> tuple[str, str]:
        if given_name and family_name:
            return given_name.strip(), family_name.strip()

        if fullname:
            fullname = fullname.strip()
            try:
                first_name, last_name = fullname.split(sep=' ', maxsplit=1)
                return first_name.strip(), last_name.strip()
            except ValueError:
                return fullname, fullname

        return 'User', uuid4().hex[:10]

    def _validate_token_response(self, response: dict) -> None:
        if 'id_token' not in response:
            raise OAuthProviderRequestError(
                provider_name=self.provider_name,
                error='invalid_oauth_response',
                error_description='id_token not found in response',
            )

    @property
    def provider_name(self) -> str:
        return SocialAccountProviders.GOOGLE

    def exchange_code(self, code: str) -> str:
        request_body = {
            'client_id': self._CLIENT_ID,
            'client_secret': self._CLIENT_SECRET,
            'code': unquote(string=code),
            'redirect_uri': self._REDIRECT_URI,
            'grant_type': self._GRANT_TYPE,
        }

        try:
            response = self.http_client.post(url=self._TOKEN_URL, data=request_body)
        except HTTPClientError as exc:
            cause = exc.__cause__
            if isinstance(cause, HTTPError) and hasattr(cause, 'response'):
                exc_response: Response = cause.response
                try:
                    response_json = exc_response.json()
                except ValueError:
                    response_json = {'raw': exc_response.text}

                error = response_json.get('error')

                if error is not None:
                    if error == 'invalid_grant':
                        raise OAuthIncorrectCodeError(provider_name=self.provider_name, code=code) from exc
                raise OAuthProviderRequestError(
                    provider_name=self.provider_name,
                    error=error,
                    error_description=response_json.get('error_description') or response_json.get('raw'),
                ) from exc
            raise

        self._validate_token_response(response=response)
        return response['id_token']

    def get_user_data(self, token: str) -> dict:
        # FIXME: handle JWT exception and raise OAuth Exception
        decoded_token = self.jwt_service.decode_unverified(token=token)

        email = decoded_token.get('email')
        if email is None:
            raise OAuthProviderEmailNotFoundError(provider_name=self.provider_name)

        provider_uid = decoded_token.get('sub')
        if provider_uid is None:
            raise OAuthProviderUidNotFoundError(provider_name=self.provider_name)

        first_name, last_name = self._get_user_names(
            given_name=decoded_token.get('given_name'),
            family_name=decoded_token.get('family_name'),
            fullname=decoded_token.get('name'),
        )

        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'provider_uid': provider_uid,
            'avatar': decoded_token.get('picture', ''),
        }
        return user_data

    def get_login_url(self, state: str) -> str:
        params = {
            'client_id': self._CLIENT_ID,
            'scope': self._SCOPE,
            'response_type': self._RESPONSE_TYPE,
            'access_type': self._ACCESS_TYPE,
            'state': state,
            'redirect_uri': self._REDIRECT_URI,
        }
        return f'{self._OAUTH_URL}?{urlencode(query=params)}'
