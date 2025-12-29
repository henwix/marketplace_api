import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.sellers.use_cases.delete import DeleteSellerUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def delete_seller_use_case(container: Container) -> DeleteSellerUseCase:
    return container.resolve(DeleteSellerUseCase)


@pytest.mark.django_db
def test_delete_seller_deleted(delete_seller_use_case: DeleteSellerUseCase, seller: Seller):
    assert Seller.objects.filter(pk=seller.pk).exists()
    delete_seller_use_case.execute(user_id=seller.user_id)
    assert not Seller.objects.filter(pk=seller.pk).exists()


@pytest.mark.django_db
def test_delete_seller_seller_not_found_error_raised(
    delete_seller_use_case: DeleteSellerUseCase,
    user: User,
):
    with pytest.raises(SellerNotFoundError):
        delete_seller_use_case.execute(user_id=user.pk)


@pytest.mark.django_db
def test_delete_seller_user_credentials_error_raised(delete_seller_use_case: DeleteSellerUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        delete_seller_use_case.execute(user_id=None)


@pytest.mark.django_db
def test_delete_seller_user_not_found_error_raised(delete_seller_use_case: DeleteSellerUseCase):
    with pytest.raises(UserNotFoundError):
        delete_seller_use_case.execute(user_id=1)


@pytest.mark.django_db
def test_delete_seller_user_not_active_error_raised(delete_seller_use_case: DeleteSellerUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        delete_seller_use_case.execute(user_id=user.pk)
