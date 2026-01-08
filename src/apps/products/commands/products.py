from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=False)
class CreateProductCommand:
    user_id: int | None
    data: dict


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
    data: dict


@dataclass(frozen=True, eq=False)
class PersonalSearchProductCommand:
    user_id: int | None
