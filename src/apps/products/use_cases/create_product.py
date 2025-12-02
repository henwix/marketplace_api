from dataclasses import dataclass

from src.apps.products.converters.products import data_to_product_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.services.products import BaseProductService


@dataclass
class CreateProductUseCase:
    service: BaseProductService

    def execute(self, seller_id: int, data: dict) -> ProductEntity:
        product_entity = data_to_product_entity(data={**data, 'seller_id': seller_id})
        product_entity.build_slug()

        new_product = self.service.create(product_entity=product_entity)
        return new_product
