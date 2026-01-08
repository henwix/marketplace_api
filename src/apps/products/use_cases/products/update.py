from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.commands.products import UpdateProductCommand
from src.apps.products.entities.products import ProductEntity
from src.apps.products.services.products import BaseProductAccessValidatorService, BaseProductService
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class UpdateProductUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService
    product_access_validator_service: BaseProductAccessValidatorService

    def execute(self, command: UpdateProductCommand) -> ProductEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=command.user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        product = self.product_service.try_get_by_id(id=command.product_id)
        self.product_access_validator_service.validate(seller=user.seller_profile, product=product)
        product.update_from_data(data=command.data)
        return self.product_service.save(product=product, update=True)
