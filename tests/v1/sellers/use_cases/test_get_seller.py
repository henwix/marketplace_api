import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.sellers.commands import GetSellerCommand
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.sellers.use_cases.get import GetSellerUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def get_seller_use_case(container: Container) -> GetSellerUseCase:
    return container.resolve(GetSellerUseCase)


@pytest.mark.django_db
def test_get_seller_retrieved(get_seller_use_case: GetSellerUseCase, seller: Seller):
    command = GetSellerCommand(user_id=seller.user_id)
    retrieved_seller = get_seller_use_case.execute(command=command)
    assert isinstance(retrieved_seller, SellerEntity)
    assert seller_to_entity(dto=seller) == retrieved_seller


@pytest.mark.django_db
def test_get_seller_seller_not_found_error_raised(
    get_seller_use_case: GetSellerUseCase,
    user: User,
):
    command = GetSellerCommand(user_id=user.pk)
    with pytest.raises(SellerNotFoundError):
        get_seller_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_seller_user_credentials_error_raised(get_seller_use_case: GetSellerUseCase):
    command = GetSellerCommand(user_id=None)
    with pytest.raises(AuthCredentialsNotProvidedError):
        get_seller_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_seller_user_not_found_error_raised(get_seller_use_case: GetSellerUseCase):
    command = GetSellerCommand(user_id=1)
    with pytest.raises(UserNotFoundError):
        get_seller_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_seller_user_not_active_error_raised(get_seller_use_case: GetSellerUseCase):
    user = UserModelFactory.create(is_active=False)
    command = GetSellerCommand(user_id=user.pk)
    with pytest.raises(UserNotActiveError):
        get_seller_use_case.execute(command=command)
