from abc import ABC, abstractmethod
from uuid import UUID

from src.apps.cart.converters import cart_item_from_entity, cart_item_to_entity, cart_to_entity
from src.apps.cart.entities import CartEntity, CartItemEntity
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
        dto = cart_item_from_entity(entity=cart_item)
        dto.save(force_update=update)
        return cart_item_to_entity(dto=dto)

    def is_cart_item_exists(self, cart_id: int, product_variant_id: UUID) -> bool:
        return CartItem.objects.filter(cart_id=cart_id, product_variant_id=product_variant_id).exists()
