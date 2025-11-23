from dataclasses import dataclass

from src.apps.users.models import User
from src.apps.users.services.users import BaseUserService


@dataclass
class SetPasswordUserUseCase:
    service: BaseUserService

    def execute(self, user: User, password: str) -> dict:
        self.service.set_password(user=user, password=password)
        return {'detail': 'Success'}
