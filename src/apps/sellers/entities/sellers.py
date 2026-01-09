from dataclasses import dataclass
from datetime import datetime

from src.apps.common.entities import BaseEntity


@dataclass(kw_only=True)
class SellerEntity(BaseEntity):
    id: int | None = None
    user_id: int
    name: str
    description: str | None = None
    avatar: str | None = None
    background: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @staticmethod
    def create(name: str, description: str | None, user_id: int) -> SellerEntity:
        return SellerEntity(
            name=name,
            description=description,
            user_id=user_id,
        )
