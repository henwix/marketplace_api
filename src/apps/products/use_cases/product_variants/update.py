from dataclasses import dataclass
from uuid import UUID

from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.services.product_variants import (
    BaseProductVariantAuthorValidatorService,
    BaseProductVariantService,
)
from src.apps.sellers.entities.sellers import SellerEntity


@dataclass
class UpdateProductVariantUseCase:
    product_variant_service: BaseProductVariantService
    author_validator_service: BaseProductVariantAuthorValidatorService

    def execute(self, seller: SellerEntity, product_variant_id: UUID, data: dict) -> ProductVariantEntity:
        product_variant = self.product_variant_service.get_by_id_with_related_product_or_404(id=product_variant_id)
        self.author_validator_service.validate(seller=seller, product_variant=product_variant)
        product_variant.update_from_data(data=data)
        return self.product_variant_service.save(product_variant=product_variant, update=True)
