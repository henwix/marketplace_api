import punq
import pytest

from src.apps.sellers.repositories.sellers import BaseSellerRepository
from src.apps.sellers.services.sellers import BaseSellerService


@pytest.fixture
def seller_repository(container: punq.Container) -> BaseSellerRepository:
    return container.resolve(BaseSellerRepository)


@pytest.fixture
def seller_service(container: punq.Container) -> BaseSellerService:
    return container.resolve(BaseSellerService)
