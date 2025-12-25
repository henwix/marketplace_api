import pytest
from punq import Container

from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.exceptions import SellerAlreadyExistsError
from src.apps.sellers.models import Seller
from src.apps.sellers.use_cases.create import CreateSellerUseCase
from src.apps.users.exceptions.users import (
    UserAuthCredentialsNotProvidedError,
    UserAuthNotActiveError,
    UserAuthNotFoundError,
)
from src.apps.users.models import User
from tests.v1.sellers.test_data.create_seller import CREATE_SELLER_ARGNAMES, CREATE_SELLER_ARGVALUES
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def create_seller_use_case(container: Container) -> CreateSellerUseCase:
    return container.resolve(CreateSellerUseCase)


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_create_seller_created(
    create_seller_use_case: CreateSellerUseCase,
    user: User,
    expected_name: str,
    expected_description: str,
):
    expected_seller_data = {
        'name': expected_name,
        'description': expected_description,
    }

    seller = create_seller_use_case.execute(user_id=user.pk, data=expected_seller_data)
    db_seller = Seller.objects.get(pk=seller.id)
    assert isinstance(seller, SellerEntity)
    assert seller_to_entity(dto=db_seller) == seller
    assert seller.user_id == user.pk
    assert seller.name == expected_name
    assert seller.description == expected_description
    assert seller.avatar is None
    assert seller.background is None


@pytest.mark.django_db
def test_create_seller_already_exists_error_raised(
    create_seller_use_case: CreateSellerUseCase,
    seller: Seller,
):
    with pytest.raises(SellerAlreadyExistsError):
        create_seller_use_case.execute(user_id=seller.user_id, data={})


@pytest.mark.django_db
def test_create_seller_user_credentials_error_raised(create_seller_use_case: CreateSellerUseCase):
    with pytest.raises(UserAuthCredentialsNotProvidedError):
        create_seller_use_case.execute(user_id=None, data={})


@pytest.mark.django_db
def test_create_seller_user_not_found_error_raised(create_seller_use_case: CreateSellerUseCase):
    with pytest.raises(UserAuthNotFoundError):
        create_seller_use_case.execute(user_id=1, data={})


@pytest.mark.django_db
def test_create_seller_user_not_active_error_raised(create_seller_use_case: CreateSellerUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserAuthNotActiveError):
        create_seller_use_case.execute(user_id=user.pk, data={})
