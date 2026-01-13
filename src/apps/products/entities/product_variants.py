from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid7

from src.apps.common.entities import BaseEntity


@dataclass(kw_only=True)
class ProductVariantEntity(BaseEntity):
    id: UUID = field(default_factory=lambda: uuid7())
    title: str
    price: Decimal
    stock: int
    is_visible: bool
    product_id: UUID
    product_seller_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @staticmethod
    def create(title: str, price: Decimal, stock: int, is_visible: bool, product_id: UUID) -> ProductVariantEntity:
        return ProductVariantEntity(
            title=title,
            price=price,
            stock=stock,
            is_visible=is_visible,
            product_id=product_id,
        )
