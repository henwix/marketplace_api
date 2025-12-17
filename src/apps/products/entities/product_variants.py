from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.apps.common.entities import BaseEntity


@dataclass(kw_only=True)
class ProductVariantEntity(BaseEntity):
    id: UUID
    product_id: UUID
    product_seller_id: int | None = None
    title: str
    price: float
    stock: int
    is_visible: int
    created_at: datetime
    updated_at: datetime
