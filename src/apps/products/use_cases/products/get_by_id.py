from dataclasses import dataclass
from uuid import UUID

from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import ProductAccessForbiddenError
from src.apps.products.services.products import BaseProductAccessValidatorService, BaseProductService
from src.apps.users.services.users import BaseUserService


@dataclass
class GetProductByIdUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    product_access_validator_service: BaseProductAccessValidatorService

    def execute(self, user_id: int | None, product_id: UUID) -> ProductEntity:
        product = self.product_service.try_get_by_id_for_retrieve(id=product_id)
        if not product.is_visible:
            if user_id is None:
                raise ProductAccessForbiddenError(product_id=product.id)
            user = self.user_service.try_get_by_id_with_loaded_seller(id=user_id)
            self.product_access_validator_service.validate(seller=user.seller_profile, product=product)
        return product
