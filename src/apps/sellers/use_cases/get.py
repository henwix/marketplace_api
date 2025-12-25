from dataclasses import dataclass

from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.services.sellers import BaseSellerDoesNotExistValidatorService
from src.apps.users.services.users import BaseUserAuthValidatorService, BaseUserService


@dataclass
class GetSellerUseCase:
    auth_validator_service: BaseUserAuthValidatorService
    user_service: BaseUserService
    seller_validator_service: BaseSellerDoesNotExistValidatorService

    def execute(self, user_id: int | None) -> SellerEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.get_by_id_with_seller_or_401(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        return user.seller_profile
