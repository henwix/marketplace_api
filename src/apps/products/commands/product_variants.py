from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.apps.common.types import UNSET, Unset


@dataclass(frozen=True, eq=False)
class CreateProductVariantCommand:
    user_id: int | None
    product_id: UUID
    title: str
    price: Decimal
    stock: int
    is_visible: bool


@dataclass(frozen=True, eq=False)
class UpdateProductVariantCommand:
    user_id: int | None
    product_variant_id: UUID
    title: str | Unset = UNSET
    price: Decimal | Unset = UNSET
    stock: int | Unset = UNSET
    is_visible: bool | Unset = UNSET


@dataclass(frozen=True, eq=False)
class DeleteProductVariantCommand:
    user_id: int | None
    product_variant_id: UUID


@dataclass(frozen=True, eq=False)
class GetProductVariantsCommand:
    user_id: int | None
    product_id: UUID
