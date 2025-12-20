import pytest
from punq import Container

from src.apps.products.repositories.products import BaseProductRepository
from src.apps.products.services.products import BaseProductAuthorValidatorService, BaseProductService


@pytest.fixture
def product_repository(container: Container) -> BaseProductRepository:
    return container.resolve(BaseProductRepository)


@pytest.fixture
def product_service(container: Container) -> BaseProductService:
    return container.resolve(BaseProductService)


@pytest.fixture
def product_author_validator_service(container: Container) -> BaseProductAuthorValidatorService:
    return container.resolve(BaseProductAuthorValidatorService)
