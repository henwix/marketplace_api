from uuid import uuid7

import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.products.exceptions.products import ProductAccessForbiddenError, ProductNotFoundByIdError
from src.apps.products.models.products import Product
from src.apps.products.use_cases.products.delete import DeleteProductUseCase
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
)
from src.apps.users.models import User
from tests.v1.products.factories import ProductModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def delete_product_use_case(container: Container) -> DeleteProductUseCase:
    return container.resolve(DeleteProductUseCase)


@pytest.mark.django_db
def test_delete_product_deleted(seller: Seller, delete_product_use_case: DeleteProductUseCase):
    product = ProductModelFactory.create(seller=seller)
    assert Product.objects.filter(pk=product.pk).exists()
    delete_product_use_case.execute(user_id=seller.user_id, product_id=product.pk)
    assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_delete_product_access_error_raised_if_seller_is_not_author(
    seller: Seller, product: Product, delete_product_use_case: DeleteProductUseCase
):
    with pytest.raises(ProductAccessForbiddenError):
        delete_product_use_case.execute(user_id=seller.user_id, product_id=product.pk)
    assert Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_delete_product_not_found_by_id_error_raised(seller: Seller, delete_product_use_case: DeleteProductUseCase):
    with pytest.raises(ProductNotFoundByIdError):
        delete_product_use_case.execute(user_id=seller.user_id, product_id=uuid7())


@pytest.mark.django_db
def test_delete_product_seller_not_found_error_raised(
    delete_product_use_case: DeleteProductUseCase,
    user: User,
):
    with pytest.raises(SellerNotFoundError):
        delete_product_use_case.execute(user_id=user.pk, product_id=uuid7())


@pytest.mark.django_db
def test_delete_product_user_credentials_error_raised(delete_product_use_case: DeleteProductUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        delete_product_use_case.execute(user_id=None, product_id=uuid7())


@pytest.mark.django_db
def test_delete_product_user_not_found_error_raised(delete_product_use_case: DeleteProductUseCase):
    with pytest.raises(UserNotFoundError):
        delete_product_use_case.execute(user_id=1, product_id=uuid7())


@pytest.mark.django_db
def test_delete_product_user_not_active_error_raised(delete_product_use_case: DeleteProductUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        delete_product_use_case.execute(user_id=user.pk, product_id=uuid7())
