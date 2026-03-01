import pytest
from punq import Container

from src.apps.cart.repositories.cart import BaseCartRepository
from src.apps.cart.services.cart import BaseCartService


@pytest.fixture
def cart_service(container: Container) -> BaseCartService:
    return container.resolve(BaseCartService)


@pytest.fixture
def cart_repository(container: Container) -> BaseCartRepository:
    return container.resolve(BaseCartRepository)
