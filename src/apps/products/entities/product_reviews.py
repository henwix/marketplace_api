from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.apps.common.entities import BaseEntity


@dataclass(kw_only=True)
class ProductReviewEntity(BaseEntity):
    id: int | None = None
    user_id: int
    product_id: UUID
    rating: int
    text: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
