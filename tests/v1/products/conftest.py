import pytest
from punq import Container

from src.apps.products.repositories.products import BaseProductRepository
from src.apps.products.services.products import BaseProductService


@pytest.fixture
def product_repository(container: Container) -> BaseProductRepository:
    return container.resolve(BaseProductRepository)


@pytest.fixture
def product_service(container: Container) -> BaseProductService:
    return container.resolve(BaseProductService)
