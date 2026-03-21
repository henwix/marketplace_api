from dataclasses import dataclass

from src.apps.authentication.commands.oauth import OAuthGetLoginUrlCommand
from src.apps.authentication.services.oauth.factory import OAuthServiceFactory


@dataclass(eq=False)
class OAuthGetLoginUrlUseCase:
    oauth_factory: OAuthServiceFactory

    def execute(self, command: OAuthGetLoginUrlCommand) -> str:
        oauth_service = self.oauth_factory.get(provider=command.provider)
        return oauth_service.get_login_url()
