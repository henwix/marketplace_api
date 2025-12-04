from dataclasses import dataclass, field
from datetime import datetime

from django.utils import timezone


@dataclass
class UserEntity:
    id: int | None = field(default=None, kw_only=True)
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str | None = field(default=None, kw_only=True)
    avatar: str | None = field(default=None, kw_only=True)
    is_staff: bool = field(default=False, kw_only=True)
    is_active: bool = field(default=True, kw_only=True)
    date_joined: datetime = field(default_factory=timezone.now, kw_only=True)
