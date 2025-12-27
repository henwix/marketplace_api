import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
)
from src.apps.users.models import User
from src.apps.users.use_cases.get import GetUserUseCase
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def get_user_use_case(container: Container) -> GetUserUseCase:
    return container.resolve(GetUserUseCase)


@pytest.mark.django_db
def test_retrieve_user_retrieved(get_user_use_case: GetUserUseCase, user: User):
    retrieved_user = get_user_use_case.execute(user_id=user.pk)
    assert isinstance(retrieved_user, UserEntity)
    assert user.pk == retrieved_user.id
    assert user.first_name == retrieved_user.first_name
    assert user.last_name == retrieved_user.last_name
    assert user.email == retrieved_user.email
    assert user.phone == retrieved_user.phone
    assert user.avatar == retrieved_user.avatar
    assert user.is_staff == retrieved_user.is_staff
    assert user.is_active == retrieved_user.is_active
    assert user.date_joined == retrieved_user.date_joined


@pytest.mark.django_db
def test_retrieve_user_user_credentials_error_raised(get_user_use_case: GetUserUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        get_user_use_case.execute(user_id=None)


@pytest.mark.django_db
def test_retrieve_user_user_not_found_error_raised(get_user_use_case: GetUserUseCase):
    with pytest.raises(UserNotFoundError):
        get_user_use_case.execute(user_id=1)


@pytest.mark.django_db
def test_retrieve_user_user_not_active_error_raised(get_user_use_case: GetUserUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        get_user_use_case.execute(user_id=user.pk)
