from abc import ABC, abstractmethod
from collections.abc import Iterable
from uuid import UUID

from django.db.models import Count, Exists, OuterRef, Prefetch, Q, Subquery

from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.converters.products import product_from_entity, product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.sellers.converters.sellers import seller_to_entity


class BaseProductRepository(ABC):
    @abstractmethod
    def save(self, product: ProductEntity, update: bool) -> ProductEntity: ...

    @abstractmethod
    def get_for_update_by_id(self, id: UUID) -> ProductEntity | None: ...

    @abstractmethod
    def get_by_id(self, id: UUID) -> ProductEntity | None: ...

    @abstractmethod
    def get_by_id_for_retrieve(self, id: UUID) -> ProductEntity | None: ...

    @abstractmethod
    def get_by_id_with_loaded_variants(self, id: UUID) -> ProductEntity | None: ...

    @abstractmethod
    def get_by_slug_for_retrieve(self, slug: str) -> ProductEntity | None: ...

    @abstractmethod
    def get_many_for_global_search(self) -> Iterable[Product]: ...

    @abstractmethod
    def get_many_for_personal_search(self, seller_id: UUID) -> Iterable[Product]: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...


class ORMProductRepository(BaseProductRepository):
    def _get_one_by_query_for_retrieve_with_relations(self, filters: Q) -> ProductEntity | None:
        dto = (
            Product.objects.filter(filters)
            .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True)))
            .select_related('seller')
        ).first()
        if dto is None:
            return None
        entity = product_to_entity(dto=dto)
        entity.seller = seller_to_entity(dto=dto.seller)
        entity.variants = [product_variant_to_entity(dto=variant) for variant in dto.variants.all()]
        return entity

    def _build_query_for_product_search(self, filters: Q, global_search: bool) -> Iterable[Product]:
        subquery = ProductVariant.objects.filter(product_id=OuterRef('pk'), is_visible=True, stock__gt=0)

        if global_search:
            qs = Product.objects.annotate(
                has_valid_variants=Exists(queryset=subquery),
                # TODO: price denormalization + price filters using FilterSet
                price=Subquery(subquery.order_by('price').values('price')[:1]),
            )
        else:
            qs = Product.objects.annotate(price=Subquery(subquery.order_by('price').values('price')[:1]))
        return qs.filter(filters)

    def save(self, product: ProductEntity, update: bool) -> ProductEntity:
        dto = product_from_entity(entity=product)
        dto.save(force_update=update)
        return product_to_entity(dto=dto)

    def get_for_update_by_id(self, id: UUID) -> ProductEntity | None:
        dto = Product.objects.select_for_update().filter(pk=id).first()
        return product_to_entity(dto=dto) if dto else None

    def get_by_id(self, id: UUID) -> ProductEntity | None:
        dto = Product.objects.filter(pk=id).first()
        return product_to_entity(dto=dto) if dto else None

    def get_by_id_for_retrieve(self, id: UUID) -> Product | None:
        return self._get_one_by_query_for_retrieve_with_relations(filters=Q(pk=id))

    def get_by_id_with_loaded_variants(self, id: UUID) -> ProductEntity | None:
        dto = (
            Product.objects.annotate(variants_count=Count('variants'))
            .filter(pk=id)
            .prefetch_related('variants')
            .first()
        )
        if dto is None:
            return None
        entity = product_to_entity(dto=dto)
        entity.variants = [product_variant_to_entity(dto=variant) for variant in dto.variants.all()]
        return entity

    def get_by_slug_for_retrieve(self, slug: str) -> Product | None:
        return self._get_one_by_query_for_retrieve_with_relations(filters=Q(slug=slug))

    def get_many_for_global_search(self) -> Iterable[Product]:
        return self._build_query_for_product_search(
            filters=Q(is_visible=True) & Q(has_valid_variants=True), global_search=True
        )

    def get_many_for_personal_search(self, seller_id: UUID) -> Iterable[Product]:
        return self._build_query_for_product_search(filters=Q(seller_id=seller_id), global_search=False)

    def delete(self, id: UUID) -> None:
        Product.objects.filter(pk=id).delete()
