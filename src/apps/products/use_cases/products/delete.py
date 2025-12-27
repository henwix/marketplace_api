from dataclasses import dataclass
from uuid import UUID

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.services.products import BaseProductAccessValidatorService, BaseProductService
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass
class DeleteProductUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService
    product_access_validator_service: BaseProductAccessValidatorService

    def execute(self, user_id: int | None, product_id: UUID) -> None:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        product = self.product_service.try_get_by_id(id=product_id)
        self.product_access_validator_service.validate(seller=user.seller_profile, product=product)
        self.product_service.delete(id=product_id)
