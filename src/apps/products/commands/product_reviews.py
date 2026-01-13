from dataclasses import dataclass
from uuid import UUID

from src.apps.common.types import UNSET, Unset


@dataclass(frozen=True, eq=False)
class CreateProductReviewCommand:
    user_id: int | None
    product_id: UUID
    rating: int
    text: str


@dataclass(frozen=True, eq=False)
class UpdateProductReviewCommand:
    user_id: int | None
    product_id: UUID
    rating: int | Unset = UNSET
    text: str | Unset = UNSET


@dataclass(frozen=True, eq=False)
class DeleteProductReviewCommand:
    user_id: int | None
    product_id: UUID


@dataclass(frozen=True, eq=False)
class GetProductReviewsCommand:
    product_id: UUID
