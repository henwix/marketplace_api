from dataclasses import dataclass
from uuid import UUID

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.services.products import (
    BaseProductAccessValidatorService,
    BaseProductHasVariantsValidatorService,
    BaseProductService,
)
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass
class GetProductVariantsUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService
    product_access_validator_service: BaseProductAccessValidatorService
    product_has_variants_validator_service: BaseProductHasVariantsValidatorService

    def execute(self, user_id: int | None, product_id: UUID) -> tuple[int, list[ProductVariantEntity]]:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        product = self.product_service.try_get_by_id_with_loaded_variants(id=product_id)
        self.product_access_validator_service.validate(seller=user.seller_profile, product=product)
        self.product_has_variants_validator_service.validate(product=product)
        return product.variants_count, product.variants
