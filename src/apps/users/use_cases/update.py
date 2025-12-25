from dataclasses import dataclass

from src.apps.users.entities import UserEntity
from src.apps.users.services.users import BaseUserAuthValidatorService, BaseUserService


@dataclass
class UpdateUserUseCase:
    auth_validator_service: BaseUserAuthValidatorService
    user_service: BaseUserService

    def execute(self, user_id: int | None, data: dict) -> UserEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.get_by_id_or_401(id=user_id)
        user.update_from_data(data=data)
        return self.user_service.save(user=user, update=True)
