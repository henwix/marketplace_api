from dataclasses import dataclass
from uuid import UUID

from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.services.product_variants import BaseProductVariantsQuantityValidatorService
from src.apps.products.services.products import BaseProductAuthorValidatorService, BaseProductService
from src.apps.sellers.entities.sellers import SellerEntity


@dataclass
class GetProductVariantsUseCase:
    product_service: BaseProductService
    author_validator_service: BaseProductAuthorValidatorService
    variants_quantity_validator_service: BaseProductVariantsQuantityValidatorService

    def execute(self, seller: SellerEntity, product_id: UUID) -> tuple[int, list[ProductVariantEntity]]:
        product = self.product_service.get_by_id_with_loaded_variants_or_404(id=product_id)
        self.author_validator_service.validate(seller=seller, product=product)
        self.variants_quantity_validator_service.validate(product=product)
        return product.variants_count, product.variants
