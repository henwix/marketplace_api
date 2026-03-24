import pytest
from django.core.cache import cache
from punq import Container

from src.apps.authentication.exceptions.oauth import OAuthIncorrectStateError
from src.apps.authentication.services.oauth.factory import OAuthServiceFactory
from src.apps.authentication.services.oauth.service import BaseOAuthService


@pytest.fixture
def mock_oauth_service_with_github_provider(mock_container: Container) -> BaseOAuthService:
    factory: OAuthServiceFactory = mock_container.resolve(OAuthServiceFactory)
    return factory.get(provider_name='github')


def test_state_created(mock_oauth_service_with_github_provider: BaseOAuthService):
    created_state = mock_oauth_service_with_github_provider.create_state()
    cache_key = f'oauth:state:github:{created_state}'
    assert isinstance(created_state, str)
    assert len(created_state) == 32
    assert cache.get(key=cache_key) == created_state


def test_state_validated(mock_oauth_service_with_github_provider: BaseOAuthService):
    created_state = mock_oauth_service_with_github_provider.create_state()
    cache_key = f'oauth:state:github:{created_state}'
    assert cache.get(key=cache_key) == created_state
    mock_oauth_service_with_github_provider.validate_state(state=created_state)
    assert cache.get(key=cache_key) is None


def test_state_not_validated_and_incorrect_state_error_raised(
    mock_oauth_service_with_github_provider: BaseOAuthService,
):
    with pytest.raises(OAuthIncorrectStateError):
        mock_oauth_service_with_github_provider.validate_state(state='123')
