from uuid import uuid7

import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.products.commands.products import UpdateProductCommand
from src.apps.products.converters.products import product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import ProductAccessForbiddenError, ProductNotFoundByIdError
from src.apps.products.models.products import Product
from src.apps.products.use_cases.products.update import UpdateProductUseCase
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
)
from src.apps.users.models import User
from tests.v1.products.factories import ProductModelFactory
from tests.v1.products.test_data.product_data import PRODUCT_ARGNAMES, PRODUCT_ARGVALUES
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def update_product_use_case(container: Container) -> UpdateProductUseCase:
    return container.resolve(UpdateProductUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_ARGNAMES, argvalues=PRODUCT_ARGVALUES)
def test_update_product_updated_by_author(
    seller: Seller,
    update_product_use_case: UpdateProductUseCase,
    expected_title: str,
    expected_desc: str,
    expected_short_desc: str,
    expected_is_visible: bool,
):
    product = ProductModelFactory.create(seller=seller)
    db_product = Product.objects.get(pk=product.pk)
    assert product == db_product

    expected_data = {
        'title': expected_title,
        'description': expected_desc,
        'short_description': expected_short_desc,
        'is_visible': expected_is_visible,
    }
    command = UpdateProductCommand(user_id=seller.user_id, product_id=product.pk, data=expected_data)
    updated_product = update_product_use_case.execute(command=command)

    assert isinstance(updated_product, ProductEntity)
    db_product = Product.objects.get(
        pk=product.pk,
        title=expected_title,
        description=expected_desc,
        short_description=expected_short_desc,
        is_visible=expected_is_visible,
    )
    assert updated_product == product_to_entity(dto=db_product)


@pytest.mark.django_db
def test_update_product_not_updated_product_access_error_raised(
    product: Product, seller: Seller, update_product_use_case: UpdateProductUseCase
):
    command = UpdateProductCommand(user_id=seller.user_id, product_id=product.pk, data={})
    with pytest.raises(ProductAccessForbiddenError):
        update_product_use_case.execute(command=command)
    db_product = Product.objects.get(pk=product.pk)
    assert db_product == product


@pytest.mark.django_db
def test_update_product_not_found_by_id_error_raised(seller: Seller, update_product_use_case: UpdateProductUseCase):
    command = UpdateProductCommand(user_id=seller.user_id, product_id=uuid7(), data={})
    with pytest.raises(ProductNotFoundByIdError):
        update_product_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_product_seller_not_found_error_raised(
    update_product_use_case: UpdateProductUseCase,
    user: User,
):
    command = UpdateProductCommand(user_id=user.pk, product_id=uuid7(), data={})
    with pytest.raises(SellerNotFoundError):
        update_product_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_product_user_credentials_error_raised(update_product_use_case: UpdateProductUseCase):
    command = UpdateProductCommand(user_id=None, product_id=uuid7(), data={})
    with pytest.raises(AuthCredentialsNotProvidedError):
        update_product_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_product_user_not_found_error_raised(update_product_use_case: UpdateProductUseCase):
    command = UpdateProductCommand(user_id=1, product_id=uuid7(), data={})
    with pytest.raises(UserNotFoundError):
        update_product_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_product_user_not_active_error_raised(update_product_use_case: UpdateProductUseCase):
    user = UserModelFactory.create(is_active=False)
    command = UpdateProductCommand(user_id=user.pk, product_id=uuid7(), data={})
    with pytest.raises(UserNotActiveError):
        update_product_use_case.execute(command=command)
