from punq import Container

from src.apps.authentication.providers.oauth.factory import BaseOAuthProviderFactory, OAuthProviderFactory
from src.apps.authentication.providers.oauth.github import OAuthGitHubProvider
from src.apps.authentication.providers.oauth.google import OAuthGoogleProvider
from src.apps.authentication.repositories.auth_providers import BaseAuthProviderRepository, ORMAuthProviderRepository
from src.apps.authentication.services.auth import AuthValidatorService, BaseAuthValidatorService
from src.apps.authentication.services.auth_providers import (
    AuthProviderMustExistValidatorService,
    AuthProviderService,
    BaseAuthProviderDisconnectValidatorService,
    BaseAuthProviderMustExistValidatorService,
    BaseAuthProviderService,
    ComposedAuthProviderDisconnectValidatorService,
    UserHasAuthProvidersValidatorService,
    UserHasAuthProviderValidatorService,
    UserMustHaseAtLeastOneAuthMethodValidatorService,
)
from src.apps.authentication.services.jwt import BaseJWTService, JWTService
from src.apps.authentication.services.oauth.factory import BaseOAuthServiceFactory, OAuthServiceFactory
from src.apps.authentication.use_cases.auth_providers.disconnect_provider import DisconnectAuthProviderUseCase
from src.apps.authentication.use_cases.auth_providers.get_connected_providers import GetConnectedAuthProvidersUseCase
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

    def _build_composed_disconnect_auth_provider_validator_service() -> BaseAuthProviderDisconnectValidatorService:
        return ComposedAuthProviderDisconnectValidatorService(
            validators=[
                container.resolve(UserHasAuthProvidersValidatorService),
                container.resolve(UserHasAuthProviderValidatorService),
                container.resolve(UserMustHaseAtLeastOneAuthMethodValidatorService),
            ]
        )

    # use_cases
    container.register(OAuthGetLoginUrlUseCase)
    container.register(OAuthVerifyUseCase)

    container.register(GetConnectedAuthProvidersUseCase)
    container.register(DisconnectAuthProviderUseCase)

    # services
    container.register(BaseAuthValidatorService, AuthValidatorService)
    container.register(BaseJWTService, JWTService)
    container.register(BaseAuthProviderService, AuthProviderService)
    container.register(
        BaseAuthProviderMustExistValidatorService,
        AuthProviderMustExistValidatorService,
    )
    container.register(UserHasAuthProvidersValidatorService)
    container.register(UserHasAuthProviderValidatorService)
    container.register(UserMustHaseAtLeastOneAuthMethodValidatorService)
    container.register(
        BaseAuthProviderDisconnectValidatorService,
        factory=_build_composed_disconnect_auth_provider_validator_service,
    )

    # service factories
    container.register(BaseOAuthServiceFactory, OAuthServiceFactory)

    # providers
    container.register(OAuthGitHubProvider)
    container.register(OAuthGoogleProvider)

    # provider factories
    container.register(BaseOAuthProviderFactory, factory=_build_oauth_provider_factory)

    # repositories
    container.register(BaseAuthProviderRepository, ORMAuthProviderRepository)
