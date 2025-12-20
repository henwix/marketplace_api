from dataclasses import dataclass, field
from datetime import datetime
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

    def build_slug(self):
        self.slug = f'{slugify(text=self.title)}-{str(self.id)[-8:]}'
