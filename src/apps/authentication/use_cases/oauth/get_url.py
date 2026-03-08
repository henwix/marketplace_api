from dataclasses import dataclass

from src.apps.authentication.services.oauth import OAuthGitHubService


@dataclass
class OAuthGitHubGetUrlUseCase:
    oauth_service: OAuthGitHubService

    def execute(self) -> str:
        return self.oauth_service.get_auth_url()
