from dataclasses import dataclass
from urllib.parse import urlencode

from django.conf import settings


@dataclass
class OAuthGitHubService:
    _AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize?'
    _ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token?'
    _API_URL = 'https://api.github.com/?'
    _CLIENT_ID = settings.GITHUB_CLIENT_ID
    _REDIRECT_URI = 'http://localhost/oauth/callback'
    _SCOPE = 'read:user user:email'
    _STATE_PREFIX = 'oauth:state:github:'

    def get_auth_url(self) -> str:
        params = {
            'client_id': self._CLIENT_ID,
            'redirect_url': self._REDIRECT_URI,
            'scope': self._SCOPE,
            'state': self.create_state(),
        }
        return self._AUTHORIZATION_URL + urlencode(query=params)

    def create_state(self) -> str:
        return '123'
