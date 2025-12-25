from dataclasses import dataclass

from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import ProductAccessForbiddenError
from src.apps.products.services.products import BaseProductAuthorValidatorService, BaseProductService
from src.apps.sellers.services.sellers import BaseSellerService
from src.apps.users.services.users import BaseUserService


@dataclass
class GetProductBySlugUseCase:
    user_service: BaseUserService
    seller_service: BaseSellerService
    product_service: BaseProductService
    product_author_validator_service: BaseProductAuthorValidatorService

    def execute(self, user_id: int | None, slug: str) -> ProductEntity:
        product = self.product_service.get_by_slug_for_retrieve_or_404(slug=slug)
        if not product.is_visible:
            if user_id is None:
                raise ProductAccessForbiddenError(product_id=product.id)
            user = self.user_service.get_by_id_with_seller_or_401(id=user_id)
            self.product_author_validator_service.validate(seller=user.seller_profile, product=product)
        return product
