from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from src.apps.products.constants import PRODUCT_VARIANTS_LIMIT
from src.apps.products.converters.product_variants import product_variant_from_entity, product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.product_variants import (
    ProductVariantAuthorPermissionError,
    ProductVariantNotFoundError,
    ProductVariantsLimitError,
    ProductVariantsNotFoundError,
)
from src.apps.products.repositories.product_variants import BaseProductVariantRepository
from src.apps.sellers.entities.sellers import SellerEntity


class BaseProductVariantAuthorValidatorService(ABC):
    @abstractmethod
    def validate(self, seller: SellerEntity | None, product_variant: ProductVariantEntity) -> None: ...


class ProductVariantAuthorValidatorService(BaseProductVariantAuthorValidatorService):
    def validate(self, seller: SellerEntity | None, product_variant: ProductVariantEntity) -> None:
        if seller is None or seller.id != product_variant.product_seller_id:
            raise ProductVariantAuthorPermissionError(
                seller_id=getattr(seller, 'id', None), product_variant_id=product_variant.id
            )


@dataclass
class BaseProductVariantLimitValidatorService(ABC):
    repository: BaseProductVariantRepository

    @abstractmethod
    def validate(self, product_id) -> None: ...


class ProductVariantLimitValidatorService(BaseProductVariantLimitValidatorService):
    def validate(self, product_id) -> None:
        variants_count = self.repository.get_variants_count(product_id=product_id)
        if variants_count >= PRODUCT_VARIANTS_LIMIT:
            raise ProductVariantsLimitError(variants_count=variants_count, variants_limit=PRODUCT_VARIANTS_LIMIT)


class BaseProductVariantsQuantityValidatorService(ABC):
    @abstractmethod
    def validate(self, product: ProductEntity) -> None: ...


class ProductVariantsQuantityValidatorService(BaseProductVariantsQuantityValidatorService):
    def validate(self, product: ProductEntity) -> None:
        if product.variants_count is not None and product.variants_count == 0:
            raise ProductVariantsNotFoundError(product_id=product.id)


@dataclass
class BaseProductVariantService(ABC):
    repository: BaseProductVariantRepository

    @abstractmethod
    def create(self, data: dict) -> ProductVariantEntity: ...

    @abstractmethod
    def save(self, product_variant: ProductVariantEntity, update: bool = False) -> ProductVariantEntity: ...

    @abstractmethod
    def get_by_id_with_related_product_or_404(self, id: UUID) -> ProductVariantEntity: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...


class ProductVariantService(BaseProductVariantService):
    def create(self, data: dict) -> ProductVariantEntity:
        dto = self.repository.create(data=data)
        return product_variant_to_entity(dto=dto)

    def save(self, product_variant: ProductVariantEntity, update: bool = False) -> ProductVariantEntity:
        dto = product_variant_from_entity(entity=product_variant)
        dto = self.repository.save(product_variant=dto, update=update)
        return product_variant_to_entity(dto=dto)

    def get_by_id_with_related_product_or_404(self, id: UUID) -> ProductVariantEntity:
        dto = self.repository.get_by_id_with_related_product_or_none(id=id)
        if dto is None:
            raise ProductVariantNotFoundError(id=id)
        return product_variant_to_entity(dto=dto)

    def delete(self, id: UUID) -> None:
        self.repository.delete(id=id)
