from dataclasses import dataclass
from uuid import UUID

from src.apps.common.types import UNSET, Unset


@dataclass(frozen=True, eq=False)
class CreateProductCommand:
    user_id: int | None
    title: str
    description: str
    short_description: str
    is_visible: bool


@dataclass(frozen=True, eq=False)
class DeleteProductCommand:
    user_id: int | None
    product_id: UUID


@dataclass(frozen=True, eq=False)
class GetProductByIdCommand:
    user_id: int | None
    product_id: UUID


@dataclass(frozen=True, eq=False)
class GetProductBySlugCommand:
    user_id: int | None
    slug: str


@dataclass(frozen=True, eq=False)
class UpdateProductCommand:
    user_id: int | None
    product_id: UUID
    title: str | Unset = UNSET
    description: str | Unset = UNSET
    short_description: str | Unset = UNSET
    is_visible: bool | Unset = UNSET


@dataclass(frozen=True, eq=False)
class PersonalSearchProductCommand:
    user_id: int | None
