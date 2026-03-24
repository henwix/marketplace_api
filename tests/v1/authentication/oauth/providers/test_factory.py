import pytest
from punq import Container

from src.apps.authentication.exceptions.oauth import OAuthNotSupportedProviderError
from src.apps.authentication.providers.oauth.factory import OAuthProviderFactory
from src.apps.authentication.providers.oauth.github import OAuthGitHubProvider


@pytest.fixture
def oauth_provider_factory(container: Container) -> OAuthProviderFactory:
    return container.resolve(OAuthProviderFactory)


def test_oauth_provider_factory_returns_correct_provider_for_github(oauth_provider_factory: OAuthProviderFactory):
    provider = oauth_provider_factory.get(provider_name='github')
    assert isinstance(provider, OAuthGitHubProvider)


def test_oauth_provider_factory_not_supported_provider_error_raised(oauth_provider_factory: OAuthProviderFactory):
    with pytest.raises(OAuthNotSupportedProviderError):
        oauth_provider_factory.get('123123123')
