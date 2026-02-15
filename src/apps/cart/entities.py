from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(kw_only=True)
class CartEntity:
    id: int
    user_id: int


@dataclass(kw_only=True)
class CartItemEntity:
    id: int | None = None
    cart_id: int
    product_variant_id: UUID
    seller_id: int
    quantity: int
    price_snapshot: Decimal
    created_at: datetime | None = None

    @staticmethod
    def create(
        cart_id: int,
        product_variant_id: UUID,
        seller_id: int,
        quantity: int,
        price_snapshot: Decimal,
    ) -> CartItemEntity:
        return CartItemEntity(
            cart_id=cart_id,
            product_variant_id=product_variant_id,
            seller_id=seller_id,
            quantity=quantity,
            price_snapshot=price_snapshot,
        )
