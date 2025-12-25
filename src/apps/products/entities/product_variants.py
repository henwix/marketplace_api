from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid7

from src.apps.common.entities import BaseEntity


@dataclass(kw_only=True)
class ProductVariantEntity(BaseEntity):
    id: UUID = field(default_factory=lambda: uuid7())
    product_id: UUID
    product_seller_id: int | None = None
    title: str
    price: float
    stock: int
    is_visible: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
