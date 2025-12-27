from dataclasses import dataclass

from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserService


@dataclass
class CreateUserUseCase:
    user_service: BaseUserService

    def execute(self, data: dict) -> UserEntity:
        return self.user_service.create(data=data)
