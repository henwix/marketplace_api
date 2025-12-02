from src.apps.products.entities.products import ProductEntity
from src.apps.products.models.products import Product


def data_to_product_entity(data: dict) -> ProductEntity:
    return ProductEntity(**data)


def product_from_entity(product_entity: ProductEntity) -> Product:
    return Product(
        pk=product_entity.uuid,
        slug=product_entity.slug,
        seller_id=product_entity.seller_id,
        title=product_entity.title,
        description=product_entity.description,
        short_description=product_entity.short_description,
        is_visible=product_entity.is_visible,
        created_at=product_entity.created_at,
        updated_at=product_entity.updated_at,
    )


def product_to_entity(dto: Product) -> ProductEntity:
    return ProductEntity(
        uuid=dto.uuid,
        slug=dto.slug,
        seller_id=dto.seller_id,
        title=dto.title,
        description=dto.description,
        short_description=dto.short_description,
        is_visible=dto.is_visible,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
    )
