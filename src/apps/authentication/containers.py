from punq import Container

from src.apps.authentication.services.auth import AuthValidatorService, BaseAuthValidatorService
from src.apps.authentication.services.oauth import OAuthGitHubService
from src.apps.authentication.use_cases.oauth.get_url import OAuthGitHubGetUrlUseCase


def init_auth(container: Container) -> None:
    # use_cases
    container.register(OAuthGitHubGetUrlUseCase)

    # services
    container.register(BaseAuthValidatorService, AuthValidatorService)
    container.register(OAuthGitHubService)
