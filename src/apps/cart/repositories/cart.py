from abc import ABC, abstractmethod
from uuid import UUID

from django.db.utils import IntegrityError

from src.apps.cart.converters import cart_item_from_entity, cart_item_to_entity, cart_to_entity
from src.apps.cart.entities import CartEntity, CartItemEntity
from src.apps.cart.exceptions import ItemAlreadyInCartError, ItemProductVariantOrSellerNotFoundError
from src.apps.cart.models import Cart, CartItem


class BaseCartRepository(ABC):
    @abstractmethod
    def get_or_create_cart(self, user_id: int) -> CartEntity: ...

    @abstractmethod
    def save_cart_item(self, cart_item: CartItemEntity, update: bool) -> CartItemEntity: ...

    @abstractmethod
    def is_cart_item_exists(self, cart_id: int, product_variant_id: UUID) -> bool: ...


class CartRepository(BaseCartRepository):
    def get_or_create_cart(self, user_id: int) -> CartEntity:
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        return cart_to_entity(dto=cart)

    def save_cart_item(self, cart_item: CartItemEntity, update: bool) -> CartItemEntity:
        try:
            dto = cart_item_from_entity(entity=cart_item)
            dto.save(force_update=update)
            return cart_item_to_entity(dto=dto)
        except IntegrityError as error:
            PG_UNIQUE_VIOLATION = '23505'
            PG_FOREIGN_KEY_VIOLATION = '23503'

            cause = error.__cause__
            if cause and getattr(cause, 'pgcode', None) == PG_UNIQUE_VIOLATION:
                raise ItemAlreadyInCartError(cart_id=cart_item.cart_id, product_variant_id=cart_item.product_variant_id)
            if cause and getattr(cause, 'pgcode', None) == PG_FOREIGN_KEY_VIOLATION:
                raise ItemProductVariantOrSellerNotFoundError(
                    cart_id=cart_item.cart_id,
                    product_variant_id=cart_item.product_variant_id,
                    seller_id=cart_item.seller_id,
                )

    def is_cart_item_exists(self, cart_id: int, product_variant_id: UUID) -> bool:
        return CartItem.objects.filter(cart_id=cart_id, product_variant_id=product_variant_id).exists()
