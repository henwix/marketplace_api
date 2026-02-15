import pytest
from punq import Container

from src.apps.cart.services.cart import BaseCartService


@pytest.fixture
def cart_service(container: Container) -> BaseCartService:
    return container.resolve(BaseCartService)
