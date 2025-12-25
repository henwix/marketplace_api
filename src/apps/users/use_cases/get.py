from dataclasses import dataclass

from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserAuthValidatorService, BaseUserService


@dataclass
class GetUserUseCase:
    auth_validator_service: BaseUserAuthValidatorService
    user_service: BaseUserService

    def execute(self, user_id: int | None) -> UserEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.get_by_id_or_401(id=user_id)
        return user
