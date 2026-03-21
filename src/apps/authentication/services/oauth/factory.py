from dataclasses import dataclass

from src.apps.authentication.providers.oauth.factory import OAuthProviderFactory
from src.apps.authentication.services.oauth.service import BaseOAuthService, OAuthService
from src.apps.common.providers.cache import BaseCacheProvider


@dataclass(eq=False)
class OAuthServiceFactory:
    provider_factory: OAuthProviderFactory
    cache_provider: BaseCacheProvider

    def get(self, provider_name: str) -> BaseOAuthService:
        provider = self.provider_factory.get(provider_name=provider_name)
        return OAuthService(cache_provider=self.cache_provider, oauth_provider=provider)
