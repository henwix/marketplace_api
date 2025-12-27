from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass
class GetSellerUseCase:
    user_service: BaseUserService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService

    def execute(self, user_id: int | None) -> SellerEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        return user.seller_profile
