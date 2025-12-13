from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.services.product_variants import (
    BaseProductVariantLimitValidatorService,
    BaseProductVariantService,
)
from src.apps.products.services.products import BaseProductAuthorValidatorService, BaseProductService
from src.apps.sellers.entities.sellers import SellerEntity


@dataclass
class CreateProductVariantUseCase:
    product_service: BaseProductService
    product_variant_service: BaseProductVariantService
    limit_validator_service: BaseProductVariantLimitValidatorService
    product_author_validator_service: BaseProductAuthorValidatorService

    def execute(self, seller: SellerEntity, data: dict, product_id: UUID) -> ProductVariantEntity:
        with transaction.atomic():
            product = self.product_service.select_for_update_by_id_or_404(id=product_id)
            self.product_author_validator_service.validate(seller=seller, product=product)
            self.limit_validator_service.validate(product_id=product_id)
            variant = self.product_variant_service.create(data={**data, 'product_id': product_id})
        return variant
