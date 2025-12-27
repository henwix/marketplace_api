import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.products.converters.products import product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.models.products import Product
from src.apps.products.use_cases.products.create import CreateProductUseCase
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
)
from src.apps.users.models import User
from tests.v1.products.test_data.product_data import PRODUCT_ARGNAMES, PRODUCT_ARGVALUES
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def create_product_use_case(container: Container) -> CreateProductUseCase:
    return container.resolve(CreateProductUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_ARGNAMES, argvalues=PRODUCT_ARGVALUES)
def test_create_product_created(
    seller: Seller,
    create_product_use_case: CreateProductUseCase,
    expected_title: str,
    expected_desc: str,
    expected_short_desc: str,
    expected_is_visible: bool,
):
    expected_data = {
        'title': expected_title,
        'description': expected_desc,
        'short_description': expected_short_desc,
        'is_visible': expected_is_visible,
    }

    created_product = create_product_use_case.execute(user_id=seller.user_id, data=expected_data)
    db_product = Product.objects.get(
        pk=created_product.id,
        title=expected_title,
        description=expected_desc,
        short_description=expected_short_desc,
        is_visible=expected_is_visible,
    )

    assert isinstance(created_product, ProductEntity)
    assert product_to_entity(dto=db_product) == created_product


@pytest.mark.django_db
def test_create_product_seller_not_found_error_raised(
    create_product_use_case: CreateProductUseCase,
    user: User,
):
    with pytest.raises(SellerNotFoundError):
        create_product_use_case.execute(user_id=user.pk, data={})


@pytest.mark.django_db
def test_create_product_user_credentials_error_raised(create_product_use_case: CreateProductUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        create_product_use_case.execute(user_id=None, data={})


@pytest.mark.django_db
def test_create_product_user_not_found_error_raised(create_product_use_case: CreateProductUseCase):
    with pytest.raises(UserNotFoundError):
        create_product_use_case.execute(user_id=1, data={})


@pytest.mark.django_db
def test_create_product_user_not_active_error_raised(create_product_use_case: CreateProductUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        create_product_use_case.execute(user_id=user.pk, data={})
