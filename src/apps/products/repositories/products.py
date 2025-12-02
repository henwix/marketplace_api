from abc import ABC, abstractmethod

from src.apps.products.models.products import Product


class BaseProductRepository(ABC):
    @abstractmethod
    def create(self, product_dto: Product) -> Product: ...


class ORMProductRepository(BaseProductRepository):
    def create(self, product_dto: Product) -> Product:
        product_dto.save()
        return product_dto
