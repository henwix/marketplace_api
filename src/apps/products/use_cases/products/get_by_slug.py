from dataclasses import dataclass

from src.apps.products.entities.products import ProductEntity
from src.apps.products.services.products import BaseProductAuthorValidatorService, BaseProductService
from src.apps.sellers.entities.sellers import SellerEntity


@dataclass
class GetProductBySlugUseCase:
    product_service: BaseProductService
    product_author_validator_service: BaseProductAuthorValidatorService

    def execute(self, seller: SellerEntity | None, slug: str) -> ProductEntity:
        product = self.product_service.get_by_slug_for_retrieve_or_404(slug=slug)
        if not product.is_visible:
            self.product_author_validator_service.validate(seller=seller, product=product)
        return product
