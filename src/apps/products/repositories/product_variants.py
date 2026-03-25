from abc import ABC, abstractmethod
from uuid import UUID

from src.apps.products.converters.product_variants import product_variant_from_entity, product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.models.product_variants import ProductVariant


class BaseProductVariantRepository(ABC):
    @abstractmethod
    def save(self, product_variant: ProductVariantEntity, update: bool) -> ProductVariantEntity: ...

    @abstractmethod
    def get_variants_count(self, product_id: UUID) -> int: ...

    @abstractmethod
    def get_by_id_with_loaded_product(self, id: UUID) -> ProductVariantEntity | None: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...


class ORMProductVariantRepository(BaseProductVariantRepository):
    def save(self, product_variant: ProductVariantEntity, update: bool) -> ProductVariantEntity:
        dto = product_variant_from_entity(entity=product_variant)
        dto.save(force_update=update)
        return product_variant_to_entity(dto=dto)

    def get_variants_count(self, product_id: UUID) -> int:
        return ProductVariant.objects.filter(product_id=product_id).count()

    def get_by_id_with_loaded_product(self, id: UUID) -> ProductVariantEntity | None:
        try:
            dto = ProductVariant.objects.select_related('product').get(pk=id)
        except ProductVariant.DoesNotExist:
            return None
        entity = product_variant_to_entity(dto=dto)
        # FIXME: use product entity instead of "product_seller_id"
        entity.product_seller_id = dto.product.seller_id
        return entity

    def delete(self, id: UUID) -> None:
        ProductVariant.objects.filter(pk=id).delete()
