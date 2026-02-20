from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from src.apps.products.constants import PRODUCT_VARIANTS_LIMIT
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.product_variants import ProductVariantsLimitError, ProductVariantsNotFoundError
from src.apps.products.exceptions.products import (
    ProductAccessForbiddenError,
    ProductNotFoundByIdError,
    ProductNotFoundBySlugError,
)
from src.apps.products.models.products import Product
from src.apps.products.repositories.product_variants import BaseProductVariantRepository
from src.apps.products.repositories.products import BaseProductRepository
from src.apps.sellers.entities.sellers import SellerEntity


class BaseProductAccessValidatorService(ABC):
    @abstractmethod
    def validate(self, seller: SellerEntity | None, product: ProductEntity) -> None: ...


class ProductAccessValidatorService(BaseProductAccessValidatorService):
    def validate(self, seller: SellerEntity | None, product: ProductEntity) -> None:
        if seller is None or seller.id != product.seller_id:
            raise ProductAccessForbiddenError(seller_id=getattr(seller, 'id', None), product_id=product.id)


class BaseProductVariantsLimitValidatorService(ABC):
    @abstractmethod
    def validate(self, product: ProductEntity) -> None: ...


@dataclass(eq=False)
class ProductVariantsLimitValidatorService(BaseProductVariantsLimitValidatorService):
    product_variant_repository: BaseProductVariantRepository

    def validate(self, product: ProductEntity) -> None:
        variants_count = self.product_variant_repository.get_variants_count(product_id=product.id)
        if variants_count is not None and variants_count >= PRODUCT_VARIANTS_LIMIT:
            raise ProductVariantsLimitError(
                product_id=product.id,
                variants_count=variants_count,
                variants_limit=PRODUCT_VARIANTS_LIMIT,
            )


class BaseProductHasVariantsValidatorService(ABC):
    @abstractmethod
    def validate(self, product: ProductEntity) -> None: ...


class ProductHasVariantsValidatorService(BaseProductHasVariantsValidatorService):
    def validate(self, product: ProductEntity) -> None:
        if product.variants_count is not None and product.variants_count == 0:
            raise ProductVariantsNotFoundError(product_id=product.id)


class BaseProductService(ABC):
    @abstractmethod
    def save(self, product: ProductEntity, update: bool = False) -> ProductEntity: ...

    @abstractmethod
    def try_get_for_update_by_id(self, id: UUID) -> ProductEntity: ...

    @abstractmethod
    def try_get_by_id(self, id: UUID) -> ProductEntity: ...

    @abstractmethod
    def try_get_by_id_for_retrieve(self, id: UUID) -> ProductEntity: ...

    @abstractmethod
    def try_get_by_id_with_loaded_variants(self, id: UUID) -> ProductEntity: ...

    @abstractmethod
    def try_get_by_slug_for_retrieve(self, slug: str) -> ProductEntity: ...

    @abstractmethod
    def get_many_for_global_search(self) -> Iterable[Product]: ...

    @abstractmethod
    def get_many_for_personal_search(self, seller_id: UUID) -> Iterable[Product]: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...


@dataclass(eq=False)
class ProductService(BaseProductService):
    repository: BaseProductRepository

    def _validate(self, product: ProductEntity | None, id: UUID) -> None:
        if product is None:
            raise ProductNotFoundByIdError(id=id)

    def save(self, product: ProductEntity, update: bool = False) -> ProductEntity:
        return self.repository.save(product=product, update=update)

    def try_get_for_update_by_id(self, id: UUID) -> ProductEntity:
        product = self.repository.get_for_update_by_id(id=id)
        self._validate(product=product, id=id)
        return product

    def try_get_by_id(self, id: UUID) -> ProductEntity:
        product = self.repository.get_by_id(id=id)
        self._validate(product=product, id=id)
        return product

    def try_get_by_id_for_retrieve(self, id: UUID) -> ProductEntity:
        product = self.repository.get_by_id_for_retrieve(id=id)
        self._validate(product=product, id=id)
        return product

    def try_get_by_id_with_loaded_variants(self, id: UUID) -> ProductEntity:
        product = self.repository.get_by_id_with_loaded_variants(id=id)
        self._validate(product=product, id=id)
        return product

    def try_get_by_slug_for_retrieve(self, slug: str) -> ProductEntity:
        product = self.repository.get_by_slug_for_retrieve(slug=slug)
        if product is None:
            raise ProductNotFoundBySlugError(slug=slug)
        return product

    def get_many_for_global_search(self) -> Iterable[Product]:
        return self.repository.get_many_for_global_search()

    def get_many_for_personal_search(self, seller_id: UUID) -> Iterable[Product]:
        return self.repository.get_many_for_personal_search(seller_id=seller_id)

    def delete(self, id: UUID) -> None:
        self.repository.delete(id=id)
