from punq import Container

from src.apps.authentication.providers.oauth.factory import BaseOAuthProviderFactory, OAuthProviderFactory
from src.apps.authentication.providers.oauth.github import OAuthGitHubProvider
from src.apps.authentication.providers.oauth.google import OAuthGoogleProvider
from src.apps.authentication.repositories.social_account import BaseSocialAccountRepository, ORMSocialAccountRepository
from src.apps.authentication.services.auth import AuthValidatorService, BaseAuthValidatorService
from src.apps.authentication.services.jwt import BaseJWTService, JWTService
from src.apps.authentication.services.oauth.factory import BaseOAuthServiceFactory, OAuthServiceFactory
from src.apps.authentication.services.social_account import BaseSocialAccountService, SocialAccountService
from src.apps.authentication.use_cases.oauth.get_url import OAuthGetLoginUrlUseCase
from src.apps.authentication.use_cases.oauth.verify import OAuthVerifyUseCase


def init_auth(container: Container) -> None:
    def _build_oauth_provider_factory() -> BaseOAuthProviderFactory:
        return OAuthProviderFactory(
            providers=[
                container.resolve(OAuthGitHubProvider),
                container.resolve(OAuthGoogleProvider),
            ]
        )

    # use_cases
    container.register(OAuthGetLoginUrlUseCase)
    container.register(OAuthVerifyUseCase)

    # services
    container.register(BaseAuthValidatorService, AuthValidatorService)
    container.register(BaseSocialAccountService, SocialAccountService)
    container.register(BaseJWTService, JWTService)

    # service factories
    container.register(BaseOAuthServiceFactory, OAuthServiceFactory)

    # providers
    container.register(OAuthGitHubProvider)
    container.register(OAuthGoogleProvider)

    # provider factories
    container.register(BaseOAuthProviderFactory, factory=_build_oauth_provider_factory)

    # repositories
    container.register(BaseSocialAccountRepository, ORMSocialAccountRepository)
