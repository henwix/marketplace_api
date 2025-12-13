from dataclasses import dataclass, field


@dataclass(kw_only=True)
class SellerEntity:
    id: int | None = field(default=None)
    user_id: int
    name: str
    description: str | None = field(default=None)
    avatar: str | None = field(default=None)
    background: str | None = field(default=None)
