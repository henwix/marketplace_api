from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.commands.product_variants import UpdateProductVariantCommand
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.services.product_variants import (
    BaseProductVariantAccessValidatorService,
    BaseProductVariantService,
)
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class UpdateProductVariantUseCase:
    user_service: BaseUserService
    variant_service: BaseProductVariantService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService
    variant_access_validator_service: BaseProductVariantAccessValidatorService

    def execute(self, command: UpdateProductVariantCommand) -> ProductVariantEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=command.user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        product_variant = self.variant_service.try_get_by_id_with_loaded_product(id=command.product_variant_id)
        self.variant_access_validator_service.validate(seller=user.seller_profile, product_variant=product_variant)
        product_variant.update_from_data(data=command.data)
        return self.variant_service.save(product_variant=product_variant, update=True)
