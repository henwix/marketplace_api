from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from src.apps.products.converters.product_variants import product_variant_from_entity, product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.exceptions.product_variants import (
    ProductVariantAccessForbiddenError,
    ProductVariantNotFoundError,
)
from src.apps.products.repositories.product_variants import BaseProductVariantRepository
from src.apps.sellers.entities.sellers import SellerEntity


class BaseProductVariantAccessValidatorService(ABC):
    @abstractmethod
    def validate(self, seller: SellerEntity | None, product_variant: ProductVariantEntity) -> None: ...


class ProductVariantAccessValidatorService(BaseProductVariantAccessValidatorService):
    def validate(self, seller: SellerEntity | None, product_variant: ProductVariantEntity) -> None:
        if seller is None or seller.id != product_variant.product_seller_id:
            raise ProductVariantAccessForbiddenError(
                seller_id=getattr(seller, 'id', None), product_variant_id=product_variant.id
            )


class BaseProductVariantService(ABC):
    @abstractmethod
    def save(self, product_variant: ProductVariantEntity, update: bool = False) -> ProductVariantEntity: ...

    @abstractmethod
    def try_get_by_id_with_loaded_product(self, id: UUID) -> ProductVariantEntity: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...


@dataclass(eq=False)
class ProductVariantService(BaseProductVariantService):
    repository: BaseProductVariantRepository

    def save(self, product_variant: ProductVariantEntity, update: bool = False) -> ProductVariantEntity:
        dto = product_variant_from_entity(entity=product_variant)
        dto = self.repository.save(product_variant=dto, update=update)
        return product_variant_to_entity(dto=dto)

    def try_get_by_id_with_loaded_product(self, id: UUID) -> ProductVariantEntity:
        dto = self.repository.get_by_id_with_loaded_product(id=id)
        if dto is None:
            raise ProductVariantNotFoundError(id=id)
        return product_variant_to_entity(dto=dto)

    def delete(self, id: UUID) -> None:
        self.repository.delete(id=id)
