from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateProductReviewCommand:
    user_id: int | None
    product_id: UUID
    data: dict


@dataclass
class UpdateProductReviewCommand:
    user_id: int | None
    product_review_id: int
    data: dict


@dataclass
class DeleteProductReviewCommand:
    user_id: int | None
    product_review_id: int
