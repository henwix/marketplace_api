from dataclasses import dataclass

from src.apps.users.models import User
from src.apps.users.services.users import BaseUserService


@dataclass
class CreateUserUseCase:
    service: BaseUserService

    def execute(self, data: dict) -> User:
        return self.service.create(data=data)
