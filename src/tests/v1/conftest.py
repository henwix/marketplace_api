import punq
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.sellers.models import Seller
from src.apps.users.models import User
from src.project.containers import get_container
from src.tests.v1.sellers.factories import SellerModelFactory
from src.tests.v1.users.factories import UserModelFactory


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
