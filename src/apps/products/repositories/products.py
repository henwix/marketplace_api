from abc import ABC, abstractmethod

from src.apps.products.models.products import Product


class BaseProductRepository(ABC):
    @abstractmethod
    def create(self, dto: Product) -> Product: ...


class ORMProductRepository(BaseProductRepository):
    def create(self, dto: Product) -> Product:
        dto.save()
        return dto
