from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.exceptions.product_variants import (
    ProductVariantAccessForbiddenError,
    ProductVariantNotFoundError,
    ProductVariantOutOfStockError,
    QuantityGreaterThanStockError,
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


class BaseProductVariantVisibilityValidatorService(ABC):
    @abstractmethod
    def validate(self, product_variant: ProductVariantEntity) -> None: ...


class ProductVariantVisibilityValidatorService(BaseProductVariantVisibilityValidatorService):
    def validate(self, product_variant: ProductVariantEntity) -> None:
        if not product_variant.is_visible:
            raise ProductVariantAccessForbiddenError(product_variant_id=product_variant.id)


class BaseProductVariantStockValidatorService(ABC):
    @abstractmethod
    def validate(self, product_variant: ProductVariantEntity, quantity: int) -> None: ...


class ProductVariantPositiveStockValidatorService(BaseProductVariantStockValidatorService):
    def validate(self, product_variant: ProductVariantEntity, *args, **kwargs) -> None:
        if product_variant.stock <= 0:
            raise ProductVariantOutOfStockError(product_variant_id=product_variant.id)


class ProductVariantAvailableQuantityValidatorService(BaseProductVariantStockValidatorService):
    def validate(self, product_variant: ProductVariantEntity, quantity: int) -> None:
        if quantity > product_variant.stock:
            raise QuantityGreaterThanStockError(
                product_variant_id=product_variant.id,
                quantity=quantity,
                stock=product_variant.stock,
            )


@dataclass
class ComposedProductVariantStockValidatorService(BaseProductVariantStockValidatorService):
    validators: list[BaseProductVariantStockValidatorService]

    def validate(self, product_variant: ProductVariantEntity, quantity: int) -> None:
        for validator in self.validators:
            validator.validate(product_variant=product_variant, quantity=quantity)


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
        product_variant = self.repository.save(product_variant=product_variant, update=update)
        return product_variant

    def try_get_by_id_with_loaded_product(self, id: UUID) -> ProductVariantEntity:
        variant = self.repository.get_by_id_with_loaded_product(id=id)
        if variant is None:
            raise ProductVariantNotFoundError(id=id)
        return variant

    def delete(self, id: UUID) -> None:
        self.repository.delete(id=id)
