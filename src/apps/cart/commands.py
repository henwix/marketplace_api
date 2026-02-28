from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=False)
class AddItemToCartCommand:
    user_id: int | None
    product_variant_id: UUID
    quantity: int


@dataclass(frozen=True, eq=False)
class GetCartCommand:
    user_id: int | None
