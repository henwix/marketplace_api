from dataclasses import dataclass

from django.db import transaction

from src.apps.authentication.commands.oauth import OAuthVerifyCommand
from src.apps.authentication.entities.auth_providers import AuthProviderEntity
from src.apps.authentication.exceptions.auth_providers import AuthProviderAlreadyConnectedError
from src.apps.authentication.services.auth_providers import BaseAuthProviderService
from src.apps.authentication.services.jwt import BaseJWTService
from src.apps.authentication.services.oauth.factory import BaseOAuthServiceFactory
from src.apps.users.services.users import (
    BaseUserService,
    BaseUserUniqueEmailValidatorService,
)


@dataclass(eq=False)
class OAuthVerifyUseCase:
    user_service: BaseUserService
    user_email_validator_service: BaseUserUniqueEmailValidatorService
    auth_provider_service: BaseAuthProviderService
    jwt_service: BaseJWTService
    oauth_service_factory: BaseOAuthServiceFactory

    def execute(self, command: OAuthVerifyCommand) -> dict[str, str]:
        oauth_service = self.oauth_service_factory.get(provider_name=command.provider)
        oauth_service.validate_state(state=command.state)
        token = oauth_service.exchange_code(code=command.code)
        user_data = oauth_service.get_user_data(token=token)
        provider_uid = user_data.get('provider_uid')

        auth_provider = self.auth_provider_service.get_by_provider_uid_and_name(
            provider_uid=provider_uid, provider=command.provider
        )

        if command.user_id is not None:
            if auth_provider is not None:
                raise AuthProviderAlreadyConnectedError(
                    current_user_id=command.user_id,
                    provider=command.provider,
                )
            user = self.user_service.try_get_active_by_id(id=command.user_id)
            new_auth_provider_entity = AuthProviderEntity.create(
                user_id=user.id,
                provider=command.provider,
                provider_uid=provider_uid,
            )
            self.auth_provider_service.save(auth_provider=new_auth_provider_entity, update=False)
            return {'detail': 'Provider successfully connected to your account'}

        if auth_provider is not None:
            user = self.user_service.try_get_active_by_id(id=auth_provider.user_id)
            tokens = self.jwt_service.create_tokens(user=user)
            return tokens

        self.user_email_validator_service.validate(email=user_data.get('email'))

        with transaction.atomic():
            user = self.user_service.create(
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                email=user_data.get('email'),
                avatar=user_data.get('avatar'),
            )
            new_auth_provider_entity = AuthProviderEntity.create(
                user_id=user.id,
                provider=command.provider,
                provider_uid=provider_uid,
            )
            self.auth_provider_service.save(auth_provider=new_auth_provider_entity, update=False)
        tokens = self.jwt_service.create_tokens(user=user)
        return tokens
