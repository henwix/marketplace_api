from dataclasses import dataclass
from uuid import UUID

from src.apps.products.entities.products import ProductEntity
from src.apps.products.services.products import BaseProductAuthorValidatorService, BaseProductService
from src.apps.sellers.entities.sellers import SellerEntity


@dataclass
class UpdateProductUseCase:
    product_service: BaseProductService
    product_author_validator_service: BaseProductAuthorValidatorService

    def execute(self, seller: SellerEntity, product_id: UUID, data: dict) -> ProductEntity:
        product = self.product_service.get_by_id_or_404(id=product_id)
        self.product_author_validator_service.validate(seller=seller, product=product)
        product.update_from_data(data=data)
        return self.product_service.save(product=product, update=True)
