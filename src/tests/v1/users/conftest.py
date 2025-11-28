import punq
import pytest

from src.apps.users.repositories.users import BaseUserRepository
from src.apps.users.services.users import BaseUserService


@pytest.fixture
def user_service(container: punq.Container) -> BaseUserService:
    return container.resolve(BaseUserService)


@pytest.fixture
def user_repository(container: punq.Container) -> BaseUserRepository:
    return container.resolve(BaseUserRepository)
