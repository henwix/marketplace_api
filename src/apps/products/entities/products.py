from dataclasses import dataclass, field
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID, uuid7

from slugify import slugify

from src.apps.common.entities import BaseEntity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.sellers.entities.sellers import SellerEntity


@dataclass(kw_only=True)
class ProductEntity(BaseEntity):
    id: UUID = field(default_factory=lambda: uuid7())
    slug: str | None = None
    seller_id: int
    seller: SellerEntity | None = None
    variants: list[ProductVariantEntity] | None = None
    variants_count: int | None = None
    title: str
    description: str | None = None
    short_description: str | None = None
    is_visible: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
    reviews_count: int = 0
    reviews_avg_rating: Decimal = 0

    def build_slug(self) -> None:
        self.slug = f'{slugify(text=self.title)}-{str(self.id)[-8:]}'

    def apply_create_review_data(self, rating: int) -> None:
        current_total_rating = self.reviews_avg_rating * self.reviews_count
        self.reviews_count += 1
        self.reviews_avg_rating = ((current_total_rating + rating) / self.reviews_count).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    def apply_update_review_data(self, old_rating: int, new_rating: int) -> None:
        current_total_rating = self.reviews_avg_rating * self.reviews_count
        current_total_rating = current_total_rating - Decimal(old_rating) + Decimal(new_rating)
        self.reviews_avg_rating = (current_total_rating / self.reviews_count).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    def apply_delete_review_data(self, rating: int) -> None:
        if self.reviews_count <= 1:
            self.reviews_count = 0
            self.reviews_avg_rating = Decimal('0')
            return

        current_total_rating = self.reviews_avg_rating * self.reviews_count
        self.reviews_count -= 1
        self.reviews_avg_rating = ((current_total_rating - rating) / self.reviews_count).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
