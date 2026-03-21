from dataclasses import dataclass

from src.apps.authentication.commands.oauth import OAuthGetLoginUrlCommand
from src.apps.authentication.services.oauth.factory import OAuthServiceFactory


@dataclass(eq=False)
class OAuthGetLoginUrlUseCase:
    oauth_service_factory: OAuthServiceFactory

    def execute(self, command: OAuthGetLoginUrlCommand) -> str:
        oauth_service = self.oauth_service_factory.get(provider_name=command.provider)
        return oauth_service.get_login_url()
