from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.converters.products import data_to_product_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.services.products import BaseProductService
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass
class CreateProductUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService

    def execute(self, user_id: int | None, data: dict) -> ProductEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user_id)
        product_entity = data_to_product_entity(data={**data, 'seller_id': user.seller_profile.id})
        product_entity.build_slug()
        new_product = self.product_service.save(product=product_entity, update=False)
        return new_product
