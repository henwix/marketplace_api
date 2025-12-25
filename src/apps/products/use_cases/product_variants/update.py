from dataclasses import dataclass
from uuid import UUID

from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.services.product_variants import (
    BaseProductVariantAuthorValidatorService,
    BaseProductVariantService,
)
from src.apps.sellers.services.sellers import BaseSellerDoesNotExistValidatorService
from src.apps.users.services.users import BaseUserAuthValidatorService, BaseUserService


@dataclass
class UpdateProductVariantUseCase:
    auth_validator_service: BaseUserAuthValidatorService
    user_service: BaseUserService
    seller_validator_service: BaseSellerDoesNotExistValidatorService
    product_variant_service: BaseProductVariantService
    author_validator_service: BaseProductVariantAuthorValidatorService

    def execute(self, user_id: int | None, product_variant_id: UUID, data: dict) -> ProductVariantEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.get_by_id_with_seller_or_401(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user_id)
        product_variant = self.product_variant_service.get_by_id_with_related_product_or_404(id=product_variant_id)
        self.author_validator_service.validate(seller=user.seller_profile, product_variant=product_variant)
        product_variant.update_from_data(data=data)
        return self.product_variant_service.save(product_variant=product_variant, update=True)
