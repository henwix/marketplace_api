import pytest
from punq import Container
from pytest_django.fixtures import SettingsWrapper
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.cart.models import Cart, CartItem
from src.apps.common.clients.http_client import BaseHTTPClient
from src.apps.products.converters.products import product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.sellers.models import Seller
from src.apps.users.models import User
from src.project.containers import _initialize_container, get_container
from tests.v1.cart.factories import CartItemModelFactory, CartModelFactory
from tests.v1.mocks.http_client import DummyHTTPClient
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
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
def cart() -> Cart:
    return CartModelFactory.create()


@pytest.fixture
def cart_item() -> CartItem:
    return CartItemModelFactory.create()


@pytest.fixture
def seller() -> Seller:
    return SellerModelFactory.create()


@pytest.fixture
def product() -> Product:
    return ProductModelFactory.create()


@pytest.fixture
def product_variant() -> ProductVariant:
    return ProductVariantModelFactory.create()


@pytest.fixture
def product_entity() -> ProductEntity:
    return product_to_entity(dto=ProductModelFactory.create())


@pytest.fixture
def container() -> Container:
    return get_container()


@pytest.fixture
def mock_container() -> Container:
    container = _initialize_container()

    container.register(BaseHTTPClient, DummyHTTPClient)

    return container


def get_client(user: User | None = None, jwt: bool = False) -> APIClient:
    client = APIClient()
    if jwt and user:
        jwt = f'Bearer {RefreshToken().for_user(user).access_token}'
        client.credentials(HTTP_AUTHORIZATION=jwt)
    return client
