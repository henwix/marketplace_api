from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.models.products import Product
from src.apps.sellers.converters.sellers import seller_to_entity


def data_to_product_entity(data: dict) -> ProductEntity:
    return ProductEntity(**data)


def product_from_entity(entity: ProductEntity) -> Product:
    return Product(
        pk=entity.id,
        slug=entity.slug,
        seller_id=entity.seller_id,
        title=entity.title,
        description=entity.description,
        short_description=entity.short_description,
        is_visible=entity.is_visible,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        reviews_count=entity.reviews_count,
        reviews_avg_rating=entity.reviews_avg_rating,
    )


def product_to_entity(dto: Product) -> ProductEntity:
    entity = ProductEntity(
        id=dto.pk,
        slug=dto.slug,
        seller_id=dto.seller_id,
        variants_count=getattr(dto, 'variants_count', None),
        title=dto.title,
        description=dto.description,
        short_description=dto.short_description,
        is_visible=dto.is_visible,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
        reviews_count=dto.reviews_count,
        reviews_avg_rating=dto.reviews_avg_rating,
    )

    if 'seller' in dto._state.fields_cache:
        entity.seller = seller_to_entity(dto=dto.seller)

    prefetched_cache = getattr(dto, '_prefetched_objects_cache', {})
    if 'variants' in prefetched_cache:
        entity.variants = [product_variant_to_entity(dto=variant) for variant in dto.variants.all()]

    return entity
