from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.products.converters.products import product_from_entity, product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.repositories.products import BaseProductRepository


@dataclass
class BaseProductService(ABC):
    repository: BaseProductRepository

    @abstractmethod
    def create(self, product_entity: ProductEntity) -> ProductEntity: ...


class ProductService(BaseProductService):
    def create(self, product_entity: ProductEntity) -> ProductEntity:
        dto = product_from_entity(product_entity=product_entity)
        dto = self.repository.create(product_dto=dto)
        return product_to_entity(dto=dto)
