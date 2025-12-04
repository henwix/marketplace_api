from dataclasses import dataclass

from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserService


@dataclass
class SetPasswordUserUseCase:
    service: BaseUserService

    def execute(self, user: UserEntity, password: str) -> dict:
        self.service.set_password(user=user, password=password)
        return {'detail': 'Success'}
