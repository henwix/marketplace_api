import pytest
from punq import Container

from src.apps.users.repositories.users import BaseUserRepository
from src.apps.users.services.users import BaseUserService


@pytest.fixture
def user_service(container: Container) -> BaseUserService:
    return container.resolve(BaseUserService)


@pytest.fixture
def user_repository(container: Container) -> BaseUserRepository:
    return container.resolve(BaseUserRepository)
