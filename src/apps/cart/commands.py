from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=False)
class AddCartItemCommand:
    user_id: int | None
    product_variant_id: UUID
    quantity: int


@dataclass(frozen=True, eq=False)
class GetCartCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class DeleteCartItemCommand:
    user_id: int | None
    product_variant_id: UUID


@dataclass(frozen=True, eq=False)
class ClearCartCommand:
    user_id: int | None
