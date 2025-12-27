from dataclasses import dataclass
from uuid import UUID

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.services.product_variants import (
    BaseProductVariantAccessValidatorService,
    BaseProductVariantService,
)
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass
class DeleteProductVariantUseCase:
    user_service: BaseUserService
    variant_service: BaseProductVariantService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService
    variant_access_validator_service: BaseProductVariantAccessValidatorService

    def execute(self, user_id: int | None, product_variant_id: UUID) -> None:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user_id)
        product_variant = self.variant_service.try_get_by_id_with_loaded_product(id=product_variant_id)
        self.variant_access_validator_service.validate(seller=user.seller_profile, product_variant=product_variant)
        self.variant_service.delete(id=product_variant_id)
