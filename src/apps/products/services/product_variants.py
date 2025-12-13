from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.products.constants import PRODUCT_VARIANTS_LIMIT
from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.exceptions.product_variants import ProductVariantsLimitError
from src.apps.products.repositories.product_variants import BaseProductVariantRepository


@dataclass
class BaseProductVariantLimitValidatorService(ABC):
    repository: BaseProductVariantRepository

    @abstractmethod
    def validate(self, product_id) -> None: ...


class ProductVariantLimitValidatorService(BaseProductVariantLimitValidatorService):
    def validate(self, product_id) -> None:
        variants_count = self.repository.get_variants_count(product_id=product_id)
        if variants_count >= PRODUCT_VARIANTS_LIMIT:
            raise ProductVariantsLimitError(variants_count=variants_count, variants_limit=PRODUCT_VARIANTS_LIMIT)


@dataclass
class BaseProductVariantService(ABC):
    repository: BaseProductVariantRepository

    @abstractmethod
    def create(self, data: dict) -> ProductVariantEntity: ...


class ProductVariantService(BaseProductVariantService):
    def create(self, data: dict) -> ProductVariantEntity:
        dto = self.repository.create(data=data)
        return product_variant_to_entity(dto=dto)
