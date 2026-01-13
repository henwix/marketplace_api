from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.apps.common.entities import BaseEntity


@dataclass(kw_only=True)
class ProductReviewEntity(BaseEntity):
    id: int | None = None
    rating: int
    text: str
    user_id: int
    product_id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @staticmethod
    def create(rating: int, text: str, user_id: int, product_id: UUID) -> ProductReviewEntity:
        return ProductReviewEntity(
            rating=rating,
            text=text,
            user_id=user_id,
            product_id=product_id,
        )
