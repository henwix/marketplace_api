import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.users.commands import DeleteUserCommand
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
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
    command = DeleteUserCommand(user_id=user.pk)
    delete_user_use_case.execute(command=command)
    assert not User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_delete_user_user_credentials_error_raised(delete_user_use_case: DeleteUserUseCase):
    command = DeleteUserCommand(user_id=None)
    with pytest.raises(AuthCredentialsNotProvidedError):
        delete_user_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_user_user_not_found_error_raised(delete_user_use_case: DeleteUserUseCase):
    command = DeleteUserCommand(user_id=1)
    with pytest.raises(UserNotFoundError):
        delete_user_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_user_user_not_active_error_raised(delete_user_use_case: DeleteUserUseCase):
    user = UserModelFactory.create(is_active=False)
    command = DeleteUserCommand(user_id=user.pk)
    with pytest.raises(UserNotActiveError):
        delete_user_use_case.execute(command=command)
