from dataclasses import dataclass

from src.apps.users.commands import CreateUserCommand
from src.apps.users.entities import UserEntity
from src.apps.users.services.users import (
    BaseUserService,
    BaseUserUniqueEmailValidatorService,
    BaseUserUniquePhoneValidatorService,
)


@dataclass(eq=False)
class CreateUserUseCase:
    user_service: BaseUserService
    user_email_validator_service: BaseUserUniqueEmailValidatorService
    user_phone_validator_service: BaseUserUniquePhoneValidatorService

    def execute(self, command: CreateUserCommand) -> UserEntity:
        self.user_email_validator_service.validate(email=command.email)
        self.user_phone_validator_service.validate(phone=command.phone)
        return self.user_service.create(
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            phone=command.phone,
            password=command.password,
        )
