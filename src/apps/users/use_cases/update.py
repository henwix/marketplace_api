from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.common.exceptions.commands import NothingToUpdateError
from src.apps.users.commands import UpdateUserCommand
from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserService, BaseUserValidatorService


@dataclass(eq=False)
class UpdateUserUseCase:
    user_service: BaseUserService
    user_validator_service: BaseUserValidatorService
    auth_validator_service: BaseAuthValidatorService

    def execute(self, command: UpdateUserCommand) -> UserEntity:
        if command.is_empty:
            raise NothingToUpdateError
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        self.user_validator_service.validate(email=command.email, phone=command.phone)
        user.update(
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            phone=command.phone,
        )
        return self.user_service.save(user=user, update=True)
