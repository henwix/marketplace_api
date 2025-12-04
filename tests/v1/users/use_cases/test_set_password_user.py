import punq
import pytest

from src.apps.users.models import User
from src.apps.users.use_cases.set_password import SetPasswordUserUseCase
from tests.v1.users.test_data.set_password_user import SET_PASSWORD_ARGNAMES, SET_PASSWORD_ARGVALUES


@pytest.fixture
def set_password_user_use_case(container: punq.Container) -> SetPasswordUserUseCase:
    return container.resolve(SetPasswordUserUseCase)


@pytest.mark.parametrize(argnames=SET_PASSWORD_ARGNAMES, argvalues=SET_PASSWORD_ARGVALUES)
@pytest.mark.django_db
def test_password_updated(
    set_password_user_use_case: SetPasswordUserUseCase,
    user: User,
    expected_password: str,
):
    """Test that the password is updated successfully"""
    assert user.check_password(expected_password) is False
    result = set_password_user_use_case.execute(user=user, password=expected_password)

    db_user = User.objects.get(pk=user.pk)
    assert db_user.check_password(expected_password) is True
    assert result == {'detail': 'Success'}
