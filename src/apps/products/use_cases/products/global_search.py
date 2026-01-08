from collections.abc import Iterable
from dataclasses import dataclass

from src.apps.products.models.products import Product
from src.apps.products.services.products import BaseProductService


@dataclass(eq=False)
class GlobalSearchProductUseCase:
    product_service: BaseProductService

    def execute(self) -> Iterable[Product]:
        products = self.product_service.get_many_for_global_search()
        return products
