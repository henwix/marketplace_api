from dataclasses import dataclass

from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserService


@dataclass
class CreateUserUseCase:
    service: BaseUserService

    def execute(self, data: dict) -> UserEntity:
        return self.service.create(data=data)
