from urllib.parse import urlencode
from uuid import uuid4

import pytest
from django.conf import settings
from punq import Container

from src.apps.authentication.constants import SocialAccountProviders
from src.apps.authentication.providers.oauth.google import OAuthGoogleProvider


@pytest.fixture
def mock_google_provider(mock_container: Container) -> OAuthGoogleProvider:
    return mock_container.resolve(OAuthGoogleProvider)


def test_get_provider_name_returns_correct_name(mock_google_provider: OAuthGoogleProvider):
    expected_provider_name = SocialAccountProviders.GOOGLE
    assert expected_provider_name == mock_google_provider.provider_name


def test_get_login_url_returns_correct_url(mock_google_provider: OAuthGoogleProvider):
    expected_state = uuid4().hex
    expected_params = {
        'client_id': settings.OAUTH_GOOGLE_CLIENT_ID,
        'scope': 'openid profile email',
        'response_type': 'code',
        'access_type': 'offline',
        'state': expected_state,
        'redirect_uri': settings.OAUTH_GOOGLE_REDIRECT_URI,
    }
    expected_login_url = f'https://accounts.google.com/o/oauth2/v2/auth?{urlencode(query=expected_params)}'
    assert expected_login_url == mock_google_provider.get_login_url(state=expected_state)


def test_exchange_code_returns_id_token_and_built_request_is_correct(mock_google_provider: OAuthGoogleProvider):
    expected_code = uuid4().hex
    expected_request = {
        'url': 'https://oauth2.googleapis.com/token',
        'params': None,
        'data': {
            'client_id': settings.OAUTH_GOOGLE_CLIENT_ID,
            'client_secret': settings.OAUTH_GOOGLE_CLIENT_SECRET,
            'code': expected_code,
            'redirect_uri': settings.OAUTH_GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        },
        'headers': None,
    }

    expected_access_token = uuid4().hex
    mock_google_provider.http_client.expected_post_responses = [{'id_token': expected_access_token}]

    access_token = mock_google_provider.exchange_code(code=expected_code)

    assert expected_access_token == access_token
    assert isinstance(access_token, str)
    assert mock_google_provider.http_client.last_requests[0] == expected_request
