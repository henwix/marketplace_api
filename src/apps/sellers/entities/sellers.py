from dataclasses import dataclass, field


@dataclass
class SellerEntity:
    id: int | None = field(default=None, kw_only=True)
    user_id: int
    name: str
    description: str | None = field(default=None, kw_only=True)
    avatar: str | None = field(default=None, kw_only=True)
    background: str | None = field(default=None, kw_only=True)
