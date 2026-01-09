import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.sellers.commands import UpdateSellerCommand
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.sellers.use_cases.update import UpdateSellerUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def update_seller_use_case(container: Container) -> UpdateSellerUseCase:
    return container.resolve(UpdateSellerUseCase)


@pytest.mark.django_db
def test_update_seller_updated(update_seller_use_case: UpdateSellerUseCase, seller: Seller):
    expected_name = 'test seller name'
    expected_description = 'test seller desc'
    command = UpdateSellerCommand(
        user_id=seller.user_id,
        name=expected_name,
        description=expected_description,
    )
    updated_seller = update_seller_use_case.execute(command=command)
    db_seller = Seller.objects.get(pk=seller.pk)

    assert isinstance(updated_seller, SellerEntity)
    assert seller_to_entity(dto=db_seller) == updated_seller
    assert db_seller.name == expected_name
    assert db_seller.description == expected_description


@pytest.mark.django_db
def test_update_seller_seller_not_found_error_raised(
    update_seller_use_case: UpdateSellerUseCase,
    user: User,
):
    command = UpdateSellerCommand(user_id=user.pk)
    with pytest.raises(SellerNotFoundError):
        update_seller_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_seller_user_credentials_error_raised(update_seller_use_case: UpdateSellerUseCase):
    command = UpdateSellerCommand(user_id=None)
    with pytest.raises(AuthCredentialsNotProvidedError):
        update_seller_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_seller_user_not_found_error_raised(update_seller_use_case: UpdateSellerUseCase):
    command = UpdateSellerCommand(user_id=1)
    with pytest.raises(UserNotFoundError):
        update_seller_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_seller_user_not_active_error_raised(update_seller_use_case: UpdateSellerUseCase):
    user = UserModelFactory.create(is_active=False)
    command = UpdateSellerCommand(user_id=user.pk)
    with pytest.raises(UserNotActiveError):
        update_seller_use_case.execute(command=command)
