from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateProductVariantCommand:
    user_id: int | None
    product_id: UUID
    data: dict


@dataclass
class DeleteProductVariantCommand:
    user_id: int | None
    product_variant_id: UUID


@dataclass
class UpdateProductVariantCommand:
    user_id: int | None
    product_variant_id: UUID
    data: dict


@dataclass
class GetProductVariantsCommand:
    user_id: int | None
    product_id: UUID
