from dataclasses import dataclass

from src.apps.authentication.exceptions.oauth import OAuthNotSupportedProviderError
from src.apps.authentication.services.oauth.base import BaseOAuthService


@dataclass(eq=False)
class OAuthServiceFactory:
    services: list[BaseOAuthService]

    def get(self, provider: str) -> BaseOAuthService:
        for service in self.services:
            if service.provider_name == provider:
                return service
        raise OAuthNotSupportedProviderError(provider_name=provider)
