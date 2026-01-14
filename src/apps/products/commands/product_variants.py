from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.apps.common.commands import BaseUpdateCommand
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
class UpdateProductVariantCommand(BaseUpdateCommand):
    user_id: int | None
    product_variant_id: UUID
    title: str | Unset = UNSET
    price: Decimal | Unset = UNSET
    stock: int | Unset = UNSET
    is_visible: bool | Unset = UNSET

    _skip_fields = {'user_id', 'product_variant_id'}


@dataclass(frozen=True, eq=False)
class DeleteProductVariantCommand:
    user_id: int | None
    product_variant_id: UUID


@dataclass(frozen=True, eq=False)
class GetProductVariantsCommand:
    user_id: int | None
    product_id: UUID
