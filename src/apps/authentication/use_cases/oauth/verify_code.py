from dataclasses import dataclass

from django.db import transaction

from src.apps.authentication.commands.oauth import OAuthVerifyCommand
from src.apps.authentication.entities.social_account import SocialAccountEntity
from src.apps.authentication.exceptions.social_account import SocialAccountProviderAlreadyConnectedError
from src.apps.authentication.services.jwt import BaseJWTService
from src.apps.authentication.services.oauth.factory import OAuthServiceFactory
from src.apps.authentication.services.social_account import BaseSocialAccountService
from src.apps.users.services.users import BaseUserService, UserUniqueEmailValidatorService


@dataclass
class OAuthVerifyUseCase:
    oauth_factory: OAuthServiceFactory
    user_service: BaseUserService
    user_unique_email_validator_service: UserUniqueEmailValidatorService
    social_account_service: BaseSocialAccountService
    jwt_service: BaseJWTService

    def execute(self, command: OAuthVerifyCommand) -> dict[str, str]:
        oauth_service = self.oauth_factory.get(provider=command.provider)

        oauth_service.validate_state(state=command.state)
        token = oauth_service.exchange_code(code=command.code)
        user_data = oauth_service.get_user_data(token=token)
        provider_uid = user_data.get('provider_uid')

        social_account = self.social_account_service.get_by_provider_uid_and_name(
            provider_uid=provider_uid, provider=oauth_service.provider_name
        )

        if command.user_id is not None:
            if social_account is not None:
                raise SocialAccountProviderAlreadyConnectedError(
                    current_user_id=command.user_id,
                    provider=oauth_service.provider_name,
                )
            user = self.user_service.try_get_active_by_id(id=command.user_id)
            new_social_account_entity = SocialAccountEntity.create(
                user_id=user.id,
                provider=oauth_service.provider_name,
                provider_uid=provider_uid,
            )
            self.social_account_service.save(social_account=new_social_account_entity, update=False)
            return {'detail': 'Provider successfully connected to your account'}

        if social_account is not None:
            user = self.user_service.try_get_active_by_id(id=social_account.user_id)
            tokens = self.jwt_service.create_tokens(user=user)
            return tokens

        # FIXME: create a new email validator or use email and phone validator separately
        self.user_unique_email_validator_service.validate(email=user_data.get('email'))

        with transaction.atomic():
            user = self.user_service.create(
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                email=user_data.get('email'),
                avatar=user_data.get('avatar'),
            )
            new_social_account_entity = SocialAccountEntity.create(
                user_id=user.id,
                provider=oauth_service.provider_name,
                provider_uid=provider_uid,
            )
            self.social_account_service.save(social_account=new_social_account_entity, update=False)
        tokens = self.jwt_service.create_tokens(user=user)
        return tokens
