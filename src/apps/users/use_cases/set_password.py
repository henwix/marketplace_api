from dataclasses import dataclass

from src.apps.users.services.users import BaseUserAuthValidatorService, BaseUserService


@dataclass
class SetPasswordUserUseCase:
    auth_validator_service: BaseUserAuthValidatorService
    service: BaseUserService

    def execute(self, user_id: int | None, password: str) -> dict:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.service.get_by_id_or_401(id=user_id)
        self.service.set_password(user=user, password=password)
        return {'detail': 'Success'}
