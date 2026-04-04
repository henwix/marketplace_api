from dataclasses import dataclass

from src.apps.authentication.commands.oauth import OAuthGetConnectedProvidersCommand
from src.apps.authentication.entities.social_account import SocialAccountEntity
from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.authentication.services.social_account import BaseSocialAccountService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class OAuthGetConnectedProvidersUseCase:
    user_service: BaseUserService
    auth_validator_service: BaseAuthValidatorService
    social_account_service: BaseSocialAccountService

    def execute(self, command: OAuthGetConnectedProvidersCommand) -> list[SocialAccountEntity]:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        return self.social_account_service.get_many_by_user_id(user_id=user.id)
