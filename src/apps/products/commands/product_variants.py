from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=False)
class CreateProductVariantCommand:
    user_id: int | None
    product_id: UUID
    data: dict


@dataclass(frozen=True, eq=False)
class DeleteProductVariantCommand:
    user_id: int | None
    product_variant_id: UUID


@dataclass(frozen=True, eq=False)
class UpdateProductVariantCommand:
    user_id: int | None
    product_variant_id: UUID
    data: dict


@dataclass(frozen=True, eq=False)
class GetProductVariantsCommand:
    user_id: int | None
    product_id: UUID
