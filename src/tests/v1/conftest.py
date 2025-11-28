import pytest

from src.apps.users.models import User
from src.tests.v1.users.factories import UserModelFactory


@pytest.fixture
def user() -> User:
    return UserModelFactory.create()
