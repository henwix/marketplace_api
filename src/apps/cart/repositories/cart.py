from abc import ABC, abstractmethod

from src.apps.cart.models import Cart


class BaseCartRepository(ABC):
    @abstractmethod
    def get_or_create(self, user_id: int) -> Cart: ...


class CartRepository(BaseCartRepository):
    def get_or_create(self, user_id: int) -> Cart:
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        return cart
