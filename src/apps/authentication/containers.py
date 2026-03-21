from punq import Container

from src.apps.authentication.repositories.social_account import BaseSocialAccountRepository, ORMSocialAccountRepository
from src.apps.authentication.services.auth import AuthValidatorService, BaseAuthValidatorService
from src.apps.authentication.services.jwt import BaseJWTService, JWTService
from src.apps.authentication.services.oauth.factory import OAuthServiceFactory
from src.apps.authentication.services.oauth.github import OAuthGitHubService
from src.apps.authentication.services.social_account import BaseSocialAccountService, SocialAccountService
from src.apps.authentication.use_cases.oauth.get_url import OAuthGetLoginUrlUseCase
from src.apps.authentication.use_cases.oauth.verify import OAuthVerifyUseCase


def init_auth(container: Container) -> None:
    def _build_oauth_service_factory() -> OAuthServiceFactory:
        return OAuthServiceFactory(
            services=[
                container.resolve(OAuthGitHubService),
            ]
        )

    # use_cases
    container.register(OAuthGetLoginUrlUseCase)
    container.register(OAuthVerifyUseCase)

    # services
    container.register(BaseAuthValidatorService, AuthValidatorService)
    container.register(OAuthGitHubService)
    container.register(OAuthServiceFactory, factory=_build_oauth_service_factory)
    container.register(BaseSocialAccountService, SocialAccountService)
    container.register(BaseJWTService, JWTService)

    # repositories
    container.register(BaseSocialAccountRepository, ORMSocialAccountRepository)
