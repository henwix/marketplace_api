from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.cart.entities import CartEntity, CartItemEntity
from src.apps.cart.exceptions import ItemAlreadyInCartError
from src.apps.cart.repositories.cart import BaseCartRepository
from src.apps.products.entities.product_variants import ProductVariantEntity


class BaseCartItemMustNotExistInCartValidatorService(ABC):
    @abstractmethod
    def validate(self, cart: CartEntity, product_variant: ProductVariantEntity) -> None: ...


@dataclass
class CartItemMustNotExistInCartValidatorService(BaseCartItemMustNotExistInCartValidatorService):
    repository: BaseCartRepository

    def validate(self, cart: CartEntity, product_variant: ProductVariantEntity) -> None:
        if self.repository.is_cart_item_exists(cart_id=cart.id, product_variant_id=product_variant.id):
            raise ItemAlreadyInCartError(cart_id=cart.id, product_variant_id=product_variant.id)


class BaseCartService(ABC):
    @abstractmethod
    def get_or_create_cart(self, user_id: int) -> CartEntity: ...

    @abstractmethod
    def save_cart_item(self, cart_item: CartItemEntity, update: bool = False) -> CartItemEntity: ...


@dataclass
class CartService(BaseCartService):
    repository: BaseCartRepository

    def get_or_create_cart(self, user_id: int) -> CartEntity:
        return self.repository.get_or_create_cart(user_id=user_id)

    def save_cart_item(self, cart_item: CartItemEntity, update: bool = False) -> CartItemEntity:
        return self.repository.save_cart_item(cart_item=cart_item, update=update)
