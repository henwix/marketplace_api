import punq
import pytest
from pytest_django.fixtures import SettingsWrapper
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.sellers.models import Seller
from src.apps.users.models import User
from src.project.containers import get_container
from tests.v1.sellers.factories import SellerModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture(autouse=True)
def disable_silk_middleware(settings: SettingsWrapper):
    """Fixture to disable Silk middleware when DEBUG == True.

    If it's enabled, it may impact test results.

    Can also be changed using the new Django settings file in pyproject.toml instead of using fixture

    """
    silk_middleware = 'silk.middleware.SilkyMiddleware'

    if silk_middleware in settings.MIDDLEWARE:
        settings.MIDDLEWARE = [i for i in settings.MIDDLEWARE if i != silk_middleware]


@pytest.fixture
def user() -> User:
    return UserModelFactory.create()


@pytest.fixture
def seller() -> Seller:
    return SellerModelFactory.create()


@pytest.fixture
def container() -> punq.Container:
    return get_container()


def get_client(user: User | None = None, jwt: bool = False) -> APIClient:
    client = APIClient()
    if jwt and user:
        jwt = f'Bearer {RefreshToken().for_user(user).access_token}'
        client.credentials(HTTP_AUTHORIZATION=jwt)
    return client
