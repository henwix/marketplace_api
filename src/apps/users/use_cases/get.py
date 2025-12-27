from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserService


@dataclass
class GetUserUseCase:
    user_service: BaseUserService
    auth_validator_service: BaseAuthValidatorService

    def execute(self, user_id: int | None) -> UserEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.try_get_by_id(id=user_id)
        return user
