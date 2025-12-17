from dataclasses import dataclass
from uuid import UUID

from src.apps.products.services.product_variants import (
    BaseProductVariantAuthorValidatorService,
    BaseProductVariantService,
)
from src.apps.sellers.entities.sellers import SellerEntity


@dataclass
class DeleteProductVariantUseCase:
    product_variant_service: BaseProductVariantService
    author_validator_service: BaseProductVariantAuthorValidatorService

    def execute(self, seller: SellerEntity, product_variant_id: UUID) -> None:
        product_variant = self.product_variant_service.get_by_id_with_related_product_or_404(id=product_variant_id)
        self.author_validator_service.validate(seller=seller, product_variant=product_variant)
        self.product_variant_service.delete(id=product_variant_id)
