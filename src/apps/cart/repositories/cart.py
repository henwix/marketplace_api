from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

from django.db.models import Count, F
from django.db.models.aggregates import Sum
from django.db.utils import IntegrityError

from src.apps.cart.converters import cart_item_from_entity, cart_item_to_entity, cart_to_entity
from src.apps.cart.entities import CartEntity, CartItemEntity
from src.apps.cart.exceptions import ItemAlreadyInCartError, ItemProductVariantOrSellerNotFoundError
from src.apps.cart.models import Cart, CartItem


class BaseCartRepository(ABC):
    @abstractmethod
    def get_or_create_cart_by_user_id_for_update(self, user_id: int) -> CartEntity: ...

    @abstractmethod
    def save_cart_item(self, cart_item: CartItemEntity, update: bool) -> CartItemEntity: ...

    @abstractmethod
    def get_cart_items_by_cart_id(self, cart_id: int) -> list[CartItemEntity]: ...

    @abstractmethod
    def get_total_cart_price(self, cart_id: int) -> Decimal | None: ...

    @abstractmethod
    def get_cart_items_count(self, cart_id: int) -> int: ...

    @abstractmethod
    def cart_item_exists(self, cart_id: int, product_variant_id: UUID) -> bool: ...

    @abstractmethod
    def delete_cart_item(self, cart_id: int, product_variant_id: UUID) -> bool: ...

    @abstractmethod
    def clear_cart(self, cart_id: int) -> bool: ...


class CartRepository(BaseCartRepository):
    def get_or_create_cart_by_user_id_for_update(self, user_id: int) -> CartEntity:
        cart = Cart.objects.select_for_update().get_or_create(user_id=user_id)[0]
        return cart_to_entity(dto=cart)

    def save_cart_item(self, cart_item: CartItemEntity, update: bool) -> CartItemEntity:
        dto = cart_item_from_entity(entity=cart_item)
        try:
            dto.save(force_update=update)
        except IntegrityError as exc:
            PG_UNIQUE_VIOLATION = '23505'
            PG_FOREIGN_KEY_VIOLATION = '23503'

            cause = exc.__cause__
            if cause and getattr(cause, 'pgcode', None) == PG_UNIQUE_VIOLATION:
                raise ItemAlreadyInCartError(
                    cart_id=cart_item.cart_id, product_variant_id=cart_item.product_variant_id
                ) from exc
            if cause and getattr(cause, 'pgcode', None) == PG_FOREIGN_KEY_VIOLATION:
                raise ItemProductVariantOrSellerNotFoundError(
                    cart_id=cart_item.cart_id,
                    product_variant_id=cart_item.product_variant_id,
                    seller_id=cart_item.seller_id,
                ) from exc
        return cart_item_to_entity(dto=dto)

    def get_cart_items_by_cart_id(self, cart_id: int) -> list[CartItemEntity]:
        items = CartItem.objects.filter(cart_id=cart_id).order_by('-created_at')
        return [cart_item_to_entity(dto=item) for item in items] if items else []

    def get_total_cart_price(self, cart_id: int) -> Decimal:
        total_price = CartItem.objects.filter(cart_id=cart_id).aggregate(
            total_price=Sum(F('price_snapshot') * F('quantity'))
        )['total_price']
        return total_price if total_price is not None else Decimal('0')

    def get_cart_items_count(self, cart_id: int) -> int:
        return CartItem.objects.filter(cart_id=cart_id).aggregate(items_count=Count('id'))['items_count']

    def cart_item_exists(self, cart_id: int, product_variant_id: UUID) -> bool:
        return CartItem.objects.filter(cart_id=cart_id, product_variant_id=product_variant_id).exists()

    def delete_cart_item(self, cart_id: int, product_variant_id: UUID) -> bool:
        return CartItem.objects.filter(cart_id=cart_id, product_variant_id=product_variant_id).delete()[0] > 0

    def clear_cart(self, cart_id: int) -> bool:
        return CartItem.objects.filter(cart_id=cart_id).delete()[0] > 0
