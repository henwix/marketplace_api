from abc import ABC, abstractmethod
from collections.abc import Iterable
from uuid import UUID

from django.db.models import Prefetch, Q

from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product


class BaseProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product, update: bool) -> Product: ...

    @abstractmethod
    def select_for_update_by_id_or_none(self, id: UUID) -> Product | None: ...

    @abstractmethod
    def get_by_id_or_none(self, id: UUID) -> Product | None: ...

    @abstractmethod
    def get_by_id_for_retrieve_or_none(self, id: UUID) -> Product | None: ...

    @abstractmethod
    def get_by_slug_for_retrieve_or_none(self, slug: str) -> Product | None: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...


class ORMProductRepository(BaseProductRepository):
    def _build_query_with_relations(self, filters: list[Q]) -> Iterable[Product]:
        return (
            Product.objects.filter(*filters)
            .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
            .select_related('seller')
        )

    def save(self, product: Product, update: bool) -> Product:
        product.save(force_update=update)
        return product

    def select_for_update_by_id_or_none(self, id: UUID) -> Product | None:
        return Product.objects.select_for_update().filter(pk=id).first()

    def get_by_id_or_none(self, id: UUID) -> Product | None:
        return Product.objects.filter(pk=id).first()

    def get_by_id_for_retrieve_or_none(self, id: UUID) -> Product | None:
        return self._build_query_with_relations(filters=[Q(pk=id)]).first()

    def get_by_slug_for_retrieve_or_none(self, slug: str) -> Product | None:
        return self._build_query_with_relations(filters=[Q(slug=slug)]).first()

    def delete(self, id: UUID) -> None:
        Product.objects.filter(pk=id).delete()
