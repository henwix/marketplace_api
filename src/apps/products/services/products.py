from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from src.apps.products.converters.products import product_from_entity, product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import (
    ProductAccessForbiddenError,
    ProductNotFoundByIdError,
    ProductNotFoundBySlugError,
)
from src.apps.products.models.products import Product
from src.apps.products.repositories.products import BaseProductRepository
from src.apps.sellers.entities.sellers import SellerEntity


class BaseProductAuthorValidatorService(ABC):
    @abstractmethod
    def validate(self, seller: SellerEntity | None, product: ProductEntity) -> None: ...


class ProductAuthorValidatorService(BaseProductAuthorValidatorService):
    def validate(self, seller: SellerEntity | None, product: ProductEntity) -> None:
        if seller is None or seller.id != product.seller_id:
            raise ProductAccessForbiddenError(seller_id=getattr(seller, 'id', None), product_id=product.id)


@dataclass
class BaseProductService(ABC):
    repository: BaseProductRepository

    @abstractmethod
    def save(self, product: ProductEntity, update: bool = False) -> ProductEntity: ...

    @abstractmethod
    def select_for_update_by_id_or_404(self, id: UUID) -> ProductEntity: ...

    @abstractmethod
    def get_by_id_or_404(self, id: UUID) -> ProductEntity: ...

    @abstractmethod
    def get_by_id_for_retrieve_or_404(self, id: UUID) -> ProductEntity: ...

    @abstractmethod
    def get_by_id_with_loaded_variants_or_404(self, id: UUID) -> ProductEntity: ...

    @abstractmethod
    def get_by_slug_for_retrieve_or_404(self, slug: str) -> ProductEntity: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...


class ProductService(BaseProductService):
    def _validate_dto(self, dto: Product | None, id: UUID) -> None:
        if dto is None:
            raise ProductNotFoundByIdError(id=id)

    def save(self, product: ProductEntity, update: bool = False) -> ProductEntity:
        dto = product_from_entity(entity=product)
        dto = self.repository.save(product=dto, update=update)
        return product_to_entity(dto=dto)

    def select_for_update_by_id_or_404(self, id: UUID) -> ProductEntity:
        dto = self.repository.select_for_update_by_id_or_none(id=id)
        self._validate_dto(dto=dto, id=id)
        return product_to_entity(dto=dto)

    def get_by_id_or_404(self, id: UUID) -> ProductEntity:
        dto = self.repository.get_by_id_or_none(id=id)
        self._validate_dto(dto=dto, id=id)
        return product_to_entity(dto=dto)

    def get_by_id_for_retrieve_or_404(self, id: UUID) -> ProductEntity:
        dto = self.repository.get_by_id_for_retrieve_or_none(id=id)
        self._validate_dto(dto=dto, id=id)
        return product_to_entity(dto=dto)

    def get_by_id_with_loaded_variants_or_404(self, id: UUID) -> ProductEntity:
        dto = self.repository.get_by_id_with_loaded_variants_or_none(id=id)
        self._validate_dto(dto=dto, id=id)
        return product_to_entity(dto=dto)

    def get_by_slug_for_retrieve_or_404(self, slug: str) -> ProductEntity:
        dto = self.repository.get_by_slug_for_retrieve_or_none(slug=slug)
        if dto is None:
            raise ProductNotFoundBySlugError(slug=slug)
        return product_to_entity(dto=dto)

    def delete(self, id: UUID) -> None:
        self.repository.delete(id=id)
