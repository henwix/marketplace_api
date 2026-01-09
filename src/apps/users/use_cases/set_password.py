from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.users.commands import SetPasswordUserCommand
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class SetPasswordUserUseCase:
    user_service: BaseUserService
    auth_validator_service: BaseAuthValidatorService

    def execute(self, command: SetPasswordUserCommand) -> None:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id(id=command.user_id)
        self.user_service.set_password(user=user, password=command.password)
