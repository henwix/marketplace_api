from dataclasses import dataclass
from uuid import UUID

from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.services.product_variants import BaseProductVariantsQuantityValidatorService
from src.apps.products.services.products import BaseProductAuthorValidatorService, BaseProductService
from src.apps.sellers.services.sellers import BaseSellerDoesNotExistValidatorService
from src.apps.users.services.users import BaseUserAuthValidatorService, BaseUserService


@dataclass
class GetProductVariantsUseCase:
    auth_validator_service: BaseUserAuthValidatorService
    user_service: BaseUserService
    seller_validator_service: BaseSellerDoesNotExistValidatorService
    product_service: BaseProductService
    author_validator_service: BaseProductAuthorValidatorService
    variants_quantity_validator_service: BaseProductVariantsQuantityValidatorService

    def execute(self, user_id: int | None, product_id: UUID) -> tuple[int, list[ProductVariantEntity]]:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.get_by_id_with_seller_or_401(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user_id)
        product = self.product_service.get_by_id_with_loaded_variants_or_404(id=product_id)
        self.author_validator_service.validate(seller=user.seller_profile, product=product)
        self.variants_quantity_validator_service.validate(product=product)
        return product.variants_count, product.variants
