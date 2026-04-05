from dataclasses import dataclass

from src.apps.authentication.commands.auth_providers import GetConnectedAuthProvidersCommand
from src.apps.authentication.entities.auth_providers import AuthProviderEntity
from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.authentication.services.auth_providers import BaseAuthProviderService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class GetConnectedAuthProvidersUseCase:
    user_service: BaseUserService
    auth_validator_service: BaseAuthValidatorService
    auth_provider_service: BaseAuthProviderService

    def execute(self, command: GetConnectedAuthProvidersCommand) -> list[AuthProviderEntity]:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        return self.auth_provider_service.get_many_by_user_id(user_id=user.id)
