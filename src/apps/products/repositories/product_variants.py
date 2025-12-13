from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from src.apps.products.models.product_variants import ProductVariant


@dataclass
class BaseProductVariantRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> ProductVariant: ...

    @abstractmethod
    def get_variants_count(self, product_id: UUID) -> int: ...


class ORMProductVariantRepository(BaseProductVariantRepository):
    def create(self, data: dict) -> ProductVariant:
        return ProductVariant.objects.create(**data)

    def get_variants_count(self, product_id: UUID) -> int:
        return ProductVariant.objects.filter(product_id=product_id).count()
