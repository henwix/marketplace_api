from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from src.apps.products.converters.product_variants import data_to_product_variant_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.services.product_variants import (
    BaseProductVariantLimitValidatorService,
    BaseProductVariantService,
)
from src.apps.products.services.products import BaseProductAuthorValidatorService, BaseProductService
from src.apps.sellers.services.sellers import BaseSellerDoesNotExistValidatorService
from src.apps.users.services.users import BaseUserAuthValidatorService, BaseUserService


@dataclass
class CreateProductVariantUseCase:
    auth_validator_service: BaseUserAuthValidatorService
    user_service: BaseUserService
    seller_validator_service: BaseSellerDoesNotExistValidatorService
    product_service: BaseProductService
    product_variant_service: BaseProductVariantService
    limit_validator_service: BaseProductVariantLimitValidatorService
    product_author_validator_service: BaseProductAuthorValidatorService

    def execute(self, user_id: int | None, product_id: UUID, data: dict) -> ProductVariantEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.get_by_id_with_seller_or_401(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user_id)
        with transaction.atomic():
            product = self.product_service.select_for_update_by_id_or_404(id=product_id)
            self.product_author_validator_service.validate(seller=user.seller_profile, product=product)
            self.limit_validator_service.validate(product_id=product_id)
            variant_entity = data_to_product_variant_entity(data={**data, 'product_id': product_id})
            new_variant = self.product_variant_service.save(product_variant=variant_entity, update=False)
        return new_variant
