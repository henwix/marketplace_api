import pytest
from punq import Container

from src.apps.sellers.repositories.sellers import BaseSellerRepository
from src.apps.sellers.services.sellers import BaseSellerService


@pytest.fixture
def seller_repository(container: Container) -> BaseSellerRepository:
    return container.resolve(BaseSellerRepository)


@pytest.fixture
def seller_service(container: Container) -> BaseSellerService:
    return container.resolve(BaseSellerService)
