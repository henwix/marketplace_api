import pytest
from punq import Container

from src.apps.users.commands import CreateUserCommand
from src.apps.users.converters import user_from_entity
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import (
    UserWithEmailAlreadyExistsError,
    UserWithPhoneAlreadyExistsError,
)
from src.apps.users.models import User
from src.apps.users.use_cases.create import CreateUserUseCase
from tests.v1.users.factories import UserModelFactory
from tests.v1.users.test_data.create_user import CREATE_USER_ARGNAMES, CREATE_USER_ARGVALUES


@pytest.fixture
def create_user_use_case(container: Container) -> CreateUserUseCase:
    return container.resolve(CreateUserUseCase)


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_create_user_created(
    create_user_use_case: CreateUserUseCase,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    """Test that a user is created successfully"""
    command = CreateUserCommand(
        first_name=expected_first_name,
        last_name=expected_last_name,
        email=expected_email,
        phone=expected_phone,
        password=expected_password,
    )
    created_user = create_user_use_case.execute(command=command)
    db_user = User.objects.get(
        pk=created_user.id,
        first_name=expected_first_name,
        last_name=expected_last_name,
        email=expected_email,
        phone=expected_phone,
    )

    assert isinstance(created_user, UserEntity)
    assert created_user.first_name == expected_first_name
    assert created_user.last_name == expected_last_name
    assert created_user.email == expected_email
    assert created_user.phone == expected_phone
    assert user_from_entity(entity=created_user).check_password(expected_password) is True
    assert db_user.check_password(expected_password) is True


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_create_user_phone_already_exists_exception_raised(
    create_user_use_case: CreateUserUseCase,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    UserModelFactory.create(phone=expected_phone)
    command = CreateUserCommand(
        first_name=expected_first_name,
        last_name=expected_last_name,
        email=expected_email,
        phone=expected_phone,
        password=expected_password,
    )
    with pytest.raises(UserWithPhoneAlreadyExistsError):
        create_user_use_case.execute(command=command)


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_create_user_email_already_exists_exception_raised(
    create_user_use_case: CreateUserUseCase,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    UserModelFactory.create(email=expected_email)
    command = CreateUserCommand(
        first_name=expected_first_name,
        last_name=expected_last_name,
        email=expected_email,
        phone=expected_phone,
        password=expected_password,
    )
    with pytest.raises(UserWithEmailAlreadyExistsError):
        create_user_use_case.execute(command=command)
