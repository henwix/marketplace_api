from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.authentication.exceptions.oauth import OAuthNotSupportedProviderError
from src.apps.authentication.providers.oauth.base import BaseOAuthProvider


class BaseOAuthProviderFactory(ABC):
    @abstractmethod
    def get(self, provider_name: str) -> BaseOAuthProvider: ...


@dataclass(eq=False)
class OAuthProviderFactory(BaseOAuthProviderFactory):
    providers: list[BaseOAuthProvider]

    def get(self, provider_name: str) -> BaseOAuthProvider:
        for provider in self.providers:
            if provider.provider_name == provider_name:
                return provider
        raise OAuthNotSupportedProviderError(provider=provider_name)
