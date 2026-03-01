from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.users.commands import GetUserCommand
from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class GetUserUseCase:
    user_service: BaseUserService
    auth_validator_service: BaseAuthValidatorService

    def execute(self, command: GetUserCommand) -> UserEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        return user
