import pytest
from punq import Container

from src.apps.products.services.product_variants import BaseProductVariantService


@pytest.fixture
def variant_service(container: Container) -> BaseProductVariantService:
    return container.resolve(BaseProductVariantService)
