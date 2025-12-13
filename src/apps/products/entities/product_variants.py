from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(kw_only=True)
class ProductVariantEntity:
    id: UUID
    product_id: UUID
    title: str
    price: float
    stock: int
    is_visible: int
    created_at: datetime
    updated_at: datetime
