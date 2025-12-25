import pytest
from punq import Container

from src.apps.users.exceptions.users import (
    UserAuthCredentialsNotProvidedError,
    UserAuthNotActiveError,
    UserAuthNotFoundError,
)
from src.apps.users.models import User
from src.apps.users.use_cases.delete import DeleteUserUseCase
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def delete_user_use_case(container: Container) -> DeleteUserUseCase:
    return container.resolve(DeleteUserUseCase)


@pytest.mark.django_db
def test_delete_user_deleted(delete_user_use_case: DeleteUserUseCase, user: User):
    assert User.objects.filter(pk=user.pk).exists()
    delete_user_use_case.execute(user_id=user.pk)
    assert not User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_delete_user_user_credentials_error_raised(delete_user_use_case: DeleteUserUseCase):
    with pytest.raises(UserAuthCredentialsNotProvidedError):
        delete_user_use_case.execute(user_id=None)


@pytest.mark.django_db
def test_delete_user_user_not_found_error_raised(delete_user_use_case: DeleteUserUseCase):
    with pytest.raises(UserAuthNotFoundError):
        delete_user_use_case.execute(user_id=1)


@pytest.mark.django_db
def test_delete_user_user_not_active_error_raised(delete_user_use_case: DeleteUserUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserAuthNotActiveError):
        delete_user_use_case.execute(user_id=user.pk)
