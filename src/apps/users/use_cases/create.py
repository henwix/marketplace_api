from dataclasses import dataclass

from src.apps.users.commands import CreateUserCommand
from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class CreateUserUseCase:
    user_service: BaseUserService

    def execute(self, command: CreateUserCommand) -> UserEntity:
        return self.user_service.create(data=command.data)
