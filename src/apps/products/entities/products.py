from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid7

from django.utils import timezone
from slugify import slugify

from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.sellers.entities.sellers import SellerEntity


@dataclass(kw_only=True)
class ProductEntity:
    id: UUID = field(default_factory=lambda: uuid7())
    slug: str | None = None
    seller_id: int
    seller: SellerEntity | None = None
    variants: list[ProductVariantEntity] | None = None
    title: str
    description: str | None = None
    short_description: str | None = None
    is_visible: bool = True
    created_at: datetime = field(default_factory=timezone.now)
    updated_at: datetime = field(default_factory=timezone.now)

    def build_slug(self):
        self.slug = f'{slugify(text=self.title)}-{str(self.id)[-8:]}'

    def update_from_data(self, data: dict) -> None:
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
