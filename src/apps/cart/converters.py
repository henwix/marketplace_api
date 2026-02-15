from src.apps.cart.entities import CartEntity, CartItemEntity
from src.apps.cart.models import Cart, CartItem


def cart_to_entity(dto: Cart) -> CartEntity:
    return CartEntity(
        id=dto.pk,
        user_id=dto.user_id,
    )


def cart_item_to_entity(dto: CartItem) -> CartItemEntity:
    return CartItemEntity(
        id=dto.pk,
        cart_id=dto.cart_id,
        product_variant_id=dto.product_variant_id,
        seller_id=dto.seller_id,
        quantity=dto.quantity,
        price_snapshot=dto.price_snapshot,
        created_at=dto.created_at,
    )


def cart_item_from_entity(entity: CartItemEntity) -> CartItem:
    return CartItem(
        pk=entity.id,
        cart_id=entity.cart_id,
        product_variant_id=entity.product_variant_id,
        seller_id=entity.seller_id,
        quantity=entity.quantity,
        price_snapshot=entity.price_snapshot,
        created_at=entity.created_at,
    )
