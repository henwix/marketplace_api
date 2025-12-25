import pytest
from punq import Container

from src.apps.users.exceptions.users import (
    UserAuthCredentialsNotProvidedError,
    UserAuthNotActiveError,
    UserAuthNotFoundError,
)
from src.apps.users.models import User
from src.apps.users.use_cases.set_password import SetPasswordUserUseCase
from tests.v1.users.factories import UserModelFactory
from tests.v1.users.test_data.set_password_user import SET_PASSWORD_ARGNAMES, SET_PASSWORD_ARGVALUES


@pytest.fixture
def set_password_user_use_case(container: Container) -> SetPasswordUserUseCase:
    return container.resolve(SetPasswordUserUseCase)


@pytest.mark.parametrize(argnames=SET_PASSWORD_ARGNAMES, argvalues=SET_PASSWORD_ARGVALUES)
@pytest.mark.django_db
def test_update_password_updated(
    set_password_user_use_case: SetPasswordUserUseCase,
    user: User,
    expected_password: str,
):
    assert user.check_password(expected_password) is False
    result = set_password_user_use_case.execute(user_id=user.pk, password=expected_password)

    db_user = User.objects.get(pk=user.pk)
    assert db_user.check_password(expected_password) is True
    assert result == {'detail': 'Success'}


@pytest.mark.django_db
def test_update_password_user_credentials_error_raised(set_password_user_use_case: SetPasswordUserUseCase):
    with pytest.raises(UserAuthCredentialsNotProvidedError):
        set_password_user_use_case.execute(user_id=None, password='123')


@pytest.mark.django_db
def test_update_password_user_not_found_error_raised(set_password_user_use_case: SetPasswordUserUseCase):
    with pytest.raises(UserAuthNotFoundError):
        set_password_user_use_case.execute(user_id=1, password='123')


@pytest.mark.django_db
def test_update_password_user_not_active_error_raised(set_password_user_use_case: SetPasswordUserUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserAuthNotActiveError):
        set_password_user_use_case.execute(user_id=user.pk, password='123')
