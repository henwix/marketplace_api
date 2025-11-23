import punq
import pytest

from src.apps.users.repositories.users import BaseUserRepository


@pytest.fixture
def user_repository(container: punq.Container) -> BaseUserRepository:
    return container.resolve(BaseUserRepository)
