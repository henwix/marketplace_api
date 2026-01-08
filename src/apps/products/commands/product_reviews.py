from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=False)
class CreateProductReviewCommand:
    user_id: int | None
    product_id: UUID
    data: dict


@dataclass(frozen=True, eq=False)
class UpdateProductReviewCommand:
    user_id: int | None
    product_id: UUID
    data: dict


@dataclass(frozen=True, eq=False)
class DeleteProductReviewCommand:
    user_id: int | None
    product_id: UUID


@dataclass(frozen=True, eq=False)
class GetProductReviewsCommand:
    product_id: UUID
