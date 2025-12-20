from dataclasses import dataclass

from src.apps.users.services.users import BaseUserService


@dataclass
class DeleteUserUseCase:
    user_service: BaseUserService

    def execute(self, user_id: int) -> None:
        self.user_service.delete(id=user_id)
