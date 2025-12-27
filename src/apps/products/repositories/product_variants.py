from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from src.apps.products.models.product_variants import ProductVariant


@dataclass
class BaseProductVariantRepository(ABC):
    @abstractmethod
    def save(self, product_variant: ProductVariant, update: bool) -> ProductVariant: ...

    @abstractmethod
    def get_variants_count(self, product_id: UUID) -> int: ...

    @abstractmethod
    def get_by_id_with_loaded_product(self, id: UUID) -> ProductVariant | None: ...

    @abstractmethod
    def delete(self, id) -> None: ...


class ORMProductVariantRepository(BaseProductVariantRepository):
    def save(self, product_variant: ProductVariant, update: bool) -> ProductVariant:
        product_variant.save(force_update=update)
        return product_variant

    def get_variants_count(self, product_id: UUID) -> int:
        return ProductVariant.objects.filter(product_id=product_id).count()

    def get_by_id_with_loaded_product(self, id: UUID) -> ProductVariant | None:
        return ProductVariant.objects.select_related('product').filter(pk=id).first()

    def delete(self, id) -> None:
        ProductVariant.objects.filter(pk=id).delete()
