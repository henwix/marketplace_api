from abc import ABC, abstractmethod
from uuid import UUID

from src.apps.cart.models import Cart, CartItem


class BaseCartRepository(ABC):
    @abstractmethod
    def get_or_create_cart(self, user_id: int) -> Cart: ...

    @abstractmethod
    def save_cart_item(self, cart_item: CartItem, update: bool) -> CartItem: ...

    @abstractmethod
    def is_item_exists(self, cart_id: int, product_variant_id: UUID) -> bool: ...


class CartRepository(BaseCartRepository):
    def get_or_create_cart(self, user_id: int) -> Cart:
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        return cart

    def save_cart_item(self, cart_item: CartItem, update: bool) -> CartItem:
        cart_item.save(force_update=update)
        return cart_item

    def is_item_exists(self, cart_id: int, product_variant_id: UUID) -> bool:
        return CartItem.objects.filter(cart_id=cart_id, product_variant_id=product_variant_id).exists()
