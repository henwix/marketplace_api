from src.apps.products.entities.products import ProductEntity
from src.apps.products.models.products import Product


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
    )


def product_to_entity(dto: Product) -> ProductEntity:
    return ProductEntity(
        id=dto.pk,
        slug=dto.slug,
        seller_id=dto.seller_id,
        title=dto.title,
        description=dto.description,
        short_description=dto.short_description,
        is_visible=dto.is_visible,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
    )
