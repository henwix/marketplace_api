from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.users.commands import UpdateUserCommand
from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserService


@dataclass
class UpdateUserUseCase:
    user_service: BaseUserService
    auth_validator_service: BaseAuthValidatorService

    def execute(self, command: UpdateUserCommand) -> UserEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id(id=command.user_id)
        user.update_from_data(data=command.data)
        return self.user_service.save(user=user, update=True)
