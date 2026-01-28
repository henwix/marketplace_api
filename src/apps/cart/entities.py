from dataclasses import dataclass


@dataclass(kw_only=True)
class CartEntity:
    id: int
    user_id: int
