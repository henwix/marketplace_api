from urllib.parse import urlencode

import pytest
from django.conf import settings
from django.core.cache import cache
from punq import Container

from src.apps.authentication.commands.oauth import OAuthGetLoginUrlCommand
from src.apps.authentication.exceptions.oauth import OAuthNotSupportedProviderError
from src.apps.authentication.use_cases.oauth.get_url import OAuthGetLoginUrlUseCase


@pytest.fixture
def oauth_get_login_url_use_case(mock_container: Container) -> OAuthGetLoginUrlUseCase:
    return mock_container.resolve(OAuthGetLoginUrlUseCase)


def test_oauth_get_login_url_returns_correct_url_and_creates_state(
    oauth_get_login_url_use_case: OAuthGetLoginUrlUseCase,
):
    command = OAuthGetLoginUrlCommand(provider='github')
    created_url = oauth_get_login_url_use_case.execute(command=command)

    state = created_url[-32:]
    cache_key = f'oauth:state:github:{state}'
    expected_params = {
        'client_id': settings.OAUTH_GITHUB_CLIENT_ID,
        'redirect_url': settings.OAUTH_GITHUB_REDIRECT_URI,
        'scope': 'read:user user:email',
        'state': state,
    }
    expected_url = f'https://github.com/login/oauth/authorize?{urlencode(query=expected_params)}'

    assert expected_url == created_url
    assert cache.get(key=cache_key) == state


def test_oauth_get_login_url_not_supported_provider_error_raised(
    oauth_get_login_url_use_case: OAuthGetLoginUrlUseCase,
):
    command = OAuthGetLoginUrlCommand(provider='123123123')
    with pytest.raises(OAuthNotSupportedProviderError):
        oauth_get_login_url_use_case.execute(command=command)
