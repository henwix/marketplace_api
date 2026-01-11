from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.commands.products import CreateProductCommand
from src.apps.products.entities.products import ProductEntity
from src.apps.products.services.products import BaseProductService
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class CreateProductUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService

    def execute(self, command: CreateProductCommand) -> ProductEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=command.user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        product_entity = ProductEntity.create(
            title=command.title,
            description=command.description,
            short_description=command.short_description,
            is_visible=command.is_visible,
            seller_id=user.seller_profile.id,
        )
        product_entity.build_slug()
        new_product = self.product_service.save(product=product_entity, update=False)
        return new_product
