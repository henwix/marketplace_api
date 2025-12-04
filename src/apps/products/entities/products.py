from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid7

from django.utils import timezone
from slugify import slugify


@dataclass
class ProductEntity:
    id: uuid7 = field(
        default_factory=lambda: str(uuid7()),
        kw_only=True,
    )
    slug: str | None = field(default=None, kw_only=True)
    seller_id: int
    title: str
    description: str | None = field(default=None, kw_only=True)
    short_description: str | None = field(default=None, kw_only=True)
    is_visible: bool = field(default=True, kw_only=True)
    created_at: datetime = field(default_factory=timezone.now, kw_only=True)
    updated_at: datetime = field(default_factory=timezone.now, kw_only=True)

    def build_slug(self):
        self.slug = f'{slugify(text=self.title)}-{self.id[-8:]}'
