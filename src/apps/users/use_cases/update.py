from dataclasses import dataclass

from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserService


@dataclass
class UpdateUserUseCase:
    user_service: BaseUserService

    def execute(self, user: UserEntity, data: dict) -> UserEntity:
        user.update_from_data(data=data)
        return self.user_service.save(user=user, update=True)
