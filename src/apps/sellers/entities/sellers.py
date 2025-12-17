from dataclasses import dataclass, field

from src.apps.common.entities import BaseEntity


@dataclass(kw_only=True)
class SellerEntity(BaseEntity):
    id: int | None = field(default=None)
    user_id: int
    name: str
    description: str | None = field(default=None)
    avatar: str | None = field(default=None)
    background: str | None = field(default=None)
