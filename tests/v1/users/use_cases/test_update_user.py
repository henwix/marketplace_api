import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.users.commands import UpdateUserCommand
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
    UserWithDataAlreadyExistsError,
)
from src.apps.users.models import User
from src.apps.users.use_cases.update import UpdateUserUseCase
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def update_user_use_case(container: Container) -> UpdateUserUseCase:
    return container.resolve(UpdateUserUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames=['expected_first_name', 'expected_last_name', 'expected_email', 'expected_phone'],
    argvalues=[
        ('New Test First Name', 'New Test Last Name', 'new_email_test@test.com', '+8761276591245'),
        ('NewTestFirstName', 'NewTestLastName', 'ajsh1924c9h1casf@test.com', '+192715125124'),
    ],
)
def test_update_user_updated(
    update_user_use_case: UpdateUserUseCase,
    user: User,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
):
    expected_data = {
        'first_name': expected_first_name,
        'last_name': expected_last_name,
        'email': expected_email,
        'phone': expected_phone,
    }
    command = UpdateUserCommand(user_id=user.pk, data=expected_data)
    updated_user = update_user_use_case.execute(command=command)
    db_user = User.objects.get(pk=user.pk)
    assert isinstance(updated_user, UserEntity)
    assert db_user.pk == updated_user.id
    assert db_user.first_name == updated_user.first_name
    assert db_user.last_name == updated_user.last_name
    assert db_user.email == updated_user.email
    assert db_user.phone == updated_user.phone
    assert db_user.avatar == updated_user.avatar
    assert db_user.is_staff == updated_user.is_staff
    assert db_user.is_active == updated_user.is_active
    assert db_user.date_joined == updated_user.date_joined


@pytest.mark.django_db
def test_update_user_phone_already_exists_error_raised(update_user_use_case: UpdateUserUseCase, user: User):
    expected_phone = '+592692652134'
    UserModelFactory.create(phone=expected_phone)

    command = UpdateUserCommand(user_id=user.pk, data={'phone': expected_phone})
    with pytest.raises(UserWithDataAlreadyExistsError):
        update_user_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_user_email_already_exists_error_raised(update_user_use_case: UpdateUserUseCase, user: User):
    expected_email = 'sdjghksdhgsg@example.com'
    UserModelFactory.create(email=expected_email)

    command = UpdateUserCommand(user_id=user.pk, data={'email': expected_email})
    with pytest.raises(UserWithDataAlreadyExistsError):
        update_user_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_user_user_credentials_error_raised(update_user_use_case: UpdateUserUseCase):
    command = UpdateUserCommand(user_id=None, data={})
    with pytest.raises(AuthCredentialsNotProvidedError):
        update_user_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_user_user_not_found_error_raised(update_user_use_case: UpdateUserUseCase):
    command = UpdateUserCommand(user_id=1, data={})
    with pytest.raises(UserNotFoundError):
        update_user_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_user_user_not_active_error_raised(update_user_use_case: UpdateUserUseCase):
    user = UserModelFactory.create(is_active=False)
    command = UpdateUserCommand(user_id=user.pk, data={})
    with pytest.raises(UserNotActiveError):
        update_user_use_case.execute(command=command)
