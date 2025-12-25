from dataclasses import dataclass
from uuid import UUID

from src.apps.products.entities.products import ProductEntity
from src.apps.products.services.products import BaseProductAuthorValidatorService, BaseProductService
from src.apps.sellers.services.sellers import BaseSellerDoesNotExistValidatorService
from src.apps.users.services.users import BaseUserAuthValidatorService, BaseUserService


@dataclass
class UpdateProductUseCase:
    auth_validator_service: BaseUserAuthValidatorService
    user_service: BaseUserService
    seller_validator_service: BaseSellerDoesNotExistValidatorService
    product_service: BaseProductService
    product_author_validator_service: BaseProductAuthorValidatorService

    def execute(self, user_id: int | None, product_id: UUID, data: dict) -> ProductEntity:
        self.auth_validator_service.validate(user_id=user_id)
        user = self.user_service.get_by_id_with_seller_or_401(id=user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        product = self.product_service.get_by_id_or_404(id=product_id)
        self.product_author_validator_service.validate(seller=user.seller_profile, product=product)
        product.update_from_data(data=data)
        return self.product_service.save(product=product, update=True)
