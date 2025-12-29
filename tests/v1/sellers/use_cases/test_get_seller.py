import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
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
    retrieved_seller = get_seller_use_case.execute(user_id=seller.user_id)
    assert isinstance(retrieved_seller, SellerEntity)
    assert seller_to_entity(dto=seller) == retrieved_seller


@pytest.mark.django_db
def test_get_seller_seller_not_found_error_raised(
    get_seller_use_case: GetSellerUseCase,
    user: User,
):
    with pytest.raises(SellerNotFoundError):
        get_seller_use_case.execute(user_id=user.pk)


@pytest.mark.django_db
def test_get_seller_user_credentials_error_raised(get_seller_use_case: GetSellerUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        get_seller_use_case.execute(user_id=None)


@pytest.mark.django_db
def test_get_seller_user_not_found_error_raised(get_seller_use_case: GetSellerUseCase):
    with pytest.raises(UserNotFoundError):
        get_seller_use_case.execute(user_id=1)


@pytest.mark.django_db
def test_get_seller_user_not_active_error_raised(get_seller_use_case: GetSellerUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        get_seller_use_case.execute(user_id=user.pk)
