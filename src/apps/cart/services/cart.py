from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.cart.converters import cart_to_entity
from src.apps.cart.entities import CartEntity
from src.apps.cart.repositories.cart import BaseCartRepository


class BaseCartService(ABC):
    @abstractmethod
    def get_or_create(self, user_id: int) -> CartEntity: ...


@dataclass
class CartService(BaseCartService):
    repository: BaseCartRepository

    def get_or_create(self, user_id: int) -> CartEntity:
        cart = self.repository.get_or_create(user_id=user_id)
        return cart_to_entity(dto=cart)
