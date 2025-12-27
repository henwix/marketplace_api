from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService, BaseSellerService
from src.apps.users.services.users import BaseUserService


@dataclass
class UpdateSellerUseCase:
    user_service: BaseUserService
    seller_service: BaseSellerService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService

    def execute(self, user_id: int | None, data: dict) -> SellerEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        user.seller_profile.update_from_data(data=data)
        return self.seller_service.save(seller=user.seller_profile, update=True)
