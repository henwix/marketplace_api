from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateProductCommand:
    user_id: int | None
    data: dict


@dataclass
class DeleteProductCommand:
    user_id: int | None
    product_id: UUID


@dataclass
class GetProductByIdCommand:
    user_id: int | None
    product_id: UUID


@dataclass
class GetProductBySlugCommand:
    user_id: int | None
    slug: str


@dataclass
class UpdateProductCommand:
    user_id: int | None
    product_id: UUID
    data: dict


@dataclass
class PersonalSearchProductCommand:
    user_id: int | None
