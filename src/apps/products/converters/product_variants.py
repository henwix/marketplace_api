from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.models.product_variants import ProductVariant


def product_variant_from_entity(entity: ProductVariantEntity) -> ProductVariant:
    return ProductVariant(
        pk=entity.id,
        product_id=entity.product_id,
        title=entity.title,
        price=entity.price,
        stock=entity.stock,
        is_visible=entity.is_visible,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def product_variant_to_entity(dto: ProductVariant) -> ProductVariantEntity:
    entity = ProductVariantEntity(
        id=dto.pk,
        product_id=dto.product_id,
        title=dto.title,
        price=dto.price,
        stock=dto.stock,
        is_visible=dto.is_visible,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
    )

    # TODO: либо маппить целый объект продукта и сохранять его в энтити, а потом уже из него получать seller_id, либо
    # сделать как-то ещё. Потому что сейчас у нас грузится по сути объект продукта, но сам его entity не сохраняется,
    # а сохраняется в отдельное поле только product_seller_id, что не логично исходя из названия самого метода, где он
    # загружается. Поменять на полный маппинг prodyct в entity и последующий его сейв в entity варианта.
    if 'product' in dto._state.fields_cache:
        entity.product_seller_id = dto.product.seller_id
    return entity
