from dataclasses import dataclass

from src.apps.products.commands.products import GetProductByIdCommand
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import ProductAccessForbiddenError
from src.apps.products.services.products import BaseProductAccessValidatorService, BaseProductService
from src.apps.users.services.users import BaseUserService


@dataclass
class GetProductByIdUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    product_access_validator_service: BaseProductAccessValidatorService

    def execute(self, command: GetProductByIdCommand) -> ProductEntity:
        product = self.product_service.try_get_by_id_for_retrieve(id=command.product_id)
        if not product.is_visible:
            if command.user_id is None:
                raise ProductAccessForbiddenError(product_id=product.id)
            user = self.user_service.try_get_by_id_with_loaded_seller(id=command.user_id)
            self.product_access_validator_service.validate(seller=user.seller_profile, product=product)
        return product
