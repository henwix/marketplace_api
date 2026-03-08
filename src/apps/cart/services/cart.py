from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.apps.cart.constants import CART_ITEMS_LIMIT
from src.apps.cart.entities import CartEntity, CartItemEntity
from src.apps.cart.exceptions import CartEmptyError, CartLimitError, ItemAlreadyInCartError, ItemNotFoundInCartError
from src.apps.cart.repositories.cart import BaseCartRepository
from src.apps.products.entities.product_variants import ProductVariantEntity


class BaseCartItemMustNotExistInCartValidatorService(ABC):
    @abstractmethod
    def validate(self, cart: CartEntity, product_variant: ProductVariantEntity) -> None: ...


@dataclass
class CartItemMustNotExistInCartValidatorService(BaseCartItemMustNotExistInCartValidatorService):
    repository: BaseCartRepository

    def validate(self, cart: CartEntity, product_variant: ProductVariantEntity) -> None:
        if self.repository.cart_item_exists(cart_id=cart.id, product_variant_id=product_variant.id):
            raise ItemAlreadyInCartError(cart_id=cart.id, product_variant_id=product_variant.id)


@dataclass
class BaseCartLimitValidatorService(ABC):
    @abstractmethod
    def validate(self, cart: CartEntity) -> None: ...


@dataclass
class CartLimitValidatorService(BaseCartLimitValidatorService):
    repository: BaseCartRepository

    def validate(self, cart: CartEntity) -> None:
        cart_items_count = self.repository.get_cart_items_count(cart_id=cart.id)
        if cart_items_count >= CART_ITEMS_LIMIT:
            raise CartLimitError(cart_id=cart.id, cart_items_count=cart_items_count, cart_items_limit=CART_ITEMS_LIMIT)


class BaseCartService(ABC):
    @abstractmethod
    def get_or_create_cart_by_user_id_for_update(self, user_id: int) -> CartEntity: ...

    @abstractmethod
    def get_total_cart_price(self, cart_id: int) -> Decimal | None: ...

    @abstractmethod
    def save_cart_item(self, cart_item: CartItemEntity, update: bool = False) -> CartItemEntity: ...

    @abstractmethod
    def get_cart_items_by_cart_id(self, cart_id: int) -> list[CartItemEntity]: ...

    @abstractmethod
    def get_cart_items_count(self, cart_id: int) -> int: ...

    @abstractmethod
    def try_delete_cart_item(self, cart_id: int, product_variant_id: UUID) -> None: ...

    @abstractmethod
    def try_clear_cart(self, cart_id: int) -> None: ...


@dataclass
class CartService(BaseCartService):
    repository: BaseCartRepository

    def get_or_create_cart_by_user_id_for_update(self, user_id: int) -> CartEntity:
        return self.repository.get_or_create_cart_by_user_id_for_update(user_id=user_id)

    def get_total_cart_price(self, cart_id: int) -> Decimal | None:
        return self.repository.get_total_cart_price(cart_id=cart_id)

    def save_cart_item(self, cart_item: CartItemEntity, update: bool = False) -> CartItemEntity:
        return self.repository.save_cart_item(cart_item=cart_item, update=update)

    def get_cart_items_by_cart_id(self, cart_id: int) -> list[CartItemEntity]:
        return self.repository.get_cart_items_by_cart_id(cart_id=cart_id)

    def get_cart_items_count(self, cart_id: int) -> int:
        return self.repository.get_cart_items_count(cart_id=cart_id)

    def try_delete_cart_item(self, cart_id: int, product_variant_id: UUID) -> None:
        is_deleted = self.repository.delete_cart_item(cart_id=cart_id, product_variant_id=product_variant_id)
        if not is_deleted:
            raise ItemNotFoundInCartError(cart_id=cart_id, product_variant_id=product_variant_id)

    def try_clear_cart(self, cart_id: int) -> None:
        is_cleared = self.repository.clear_cart(cart_id=cart_id)
        if not is_cleared:
            raise CartEmptyError(cart_id=cart_id)
