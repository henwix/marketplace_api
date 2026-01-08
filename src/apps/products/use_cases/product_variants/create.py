from dataclasses import dataclass

from django.db import transaction

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.commands.product_variants import CreateProductVariantCommand
from src.apps.products.converters.product_variants import data_to_product_variant_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.services.product_variants import (
    BaseProductVariantService,
)
from src.apps.products.services.products import (
    BaseProductAccessValidatorService,
    BaseProductService,
    BaseProductVariantsLimitValidatorService,
)
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class CreateProductVariantUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    variant_service: BaseProductVariantService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService
    product_access_validator_service: BaseProductAccessValidatorService
    variants_limit_validator_service: BaseProductVariantsLimitValidatorService

    def execute(self, command: CreateProductVariantCommand) -> ProductVariantEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=command.user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        with transaction.atomic():
            product = self.product_service.try_get_for_update_by_id(id=command.product_id)
            self.product_access_validator_service.validate(seller=user.seller_profile, product=product)
            self.variants_limit_validator_service.validate(product=product)
            variant_entity = data_to_product_variant_entity(data={**command.data, 'product_id': product.id})
            new_variant = self.variant_service.save(product_variant=variant_entity, update=False)
        return new_variant
