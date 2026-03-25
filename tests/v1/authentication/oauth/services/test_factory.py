import pytest
from punq import Container

from src.apps.authentication.exceptions.oauth import OAuthNotSupportedProviderError
from src.apps.authentication.providers.oauth.github import OAuthGitHubProvider
from src.apps.authentication.services.oauth.factory import BaseOAuthServiceFactory
from src.apps.authentication.services.oauth.service import OAuthService
from src.apps.common.providers.cache import BaseCacheProvider


@pytest.fixture
def oauth_service_factory(container: Container) -> BaseOAuthServiceFactory:
    return container.resolve(BaseOAuthServiceFactory)


def test_oauth_service_factory_returns_service_with_correct_provider_for_github(
    oauth_service_factory: BaseOAuthServiceFactory,
):
    service = oauth_service_factory.get(provider_name='github')
    assert isinstance(service, OAuthService)
    assert isinstance(service.cache_provider, BaseCacheProvider)
    assert isinstance(service.oauth_provider, OAuthGitHubProvider)


def test_oauth_service_factory_not_supported_provider_error_raised(oauth_service_factory: BaseOAuthServiceFactory):
    with pytest.raises(OAuthNotSupportedProviderError):
        oauth_service_factory.get('123123123')
