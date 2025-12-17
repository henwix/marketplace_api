from dataclasses import dataclass, field
from datetime import datetime

from django.utils import timezone

from src.apps.common.entities import BaseEntity


@dataclass(kw_only=True)
class UserEntity(BaseEntity):
    id: int | None = field(default=None)
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str | None = field(default=None)
    avatar: str | None = field(default=None)
    is_staff: bool = field(default=False)
    is_active: bool = field(default=True)
    date_joined: datetime = field(default_factory=timezone.now)
