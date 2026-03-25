from dataclasses import dataclass
from datetime import datetime

from src.apps.common.entities import BaseEntity
from src.apps.sellers.entities.sellers import SellerEntity


@dataclass(kw_only=True)
class UserEntity(BaseEntity):
    id: int | None = None
    seller_profile: SellerEntity | None = None
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    password: str | None = None
    avatar: str | None = None
    is_staff: bool = False
    is_active: bool = True
    date_joined: datetime | None = None
