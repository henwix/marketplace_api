import pytest

from src.apps.users.exceptions.users import UserWithDataAlreadyExistsError
from src.apps.users.models import User
from src.apps.users.services.users import BaseUserService
from src.tests.v1.users.factories.users import UserModelFactory
from src.tests.v1.users.test_data.create_user import CREATE_USER_ARGNAMES, CREATE_USER_ARGVALUES
from src.tests.v1.users.test_data.set_password_user import SET_PASSWORD_ARGNAMES, SET_PASSWORD_ARGVALUES


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_user_created(
    user_service: BaseUserService,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    """Test that a user is created successfully"""
    created_user = user_service.create(
        data={
            'first_name': expected_first_name,
            'last_name': expected_last_name,
            'email': expected_email,
            'phone': expected_phone,
            'password': expected_password,
        },
    )

    assert created_user.first_name == expected_first_name
    assert created_user.last_name == expected_last_name
    assert created_user.email == expected_email
    assert created_user.phone == expected_phone
    assert created_user.check_password(expected_password) is True


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_user_create_email_already_exists_error(
    user_service: BaseUserService,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    """Test that creating a user with an existing email raises an error"""
    UserModelFactory.create(email=expected_email)

    with pytest.raises(UserWithDataAlreadyExistsError):
        user_service.create(
            data={
                'first_name': expected_first_name,
                'last_name': expected_last_name,
                'email': expected_email,
                'phone': expected_phone,
                'password': expected_password,
            },
        )


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_user_create_phone_already_exists_error(
    user_service: BaseUserService,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    """Test that creating a user with an existing phone raises an error"""
    UserModelFactory.create(phone=expected_phone)

    with pytest.raises(UserWithDataAlreadyExistsError):
        user_service.create(
            data={
                'first_name': expected_first_name,
                'last_name': expected_last_name,
                'email': expected_email,
                'phone': expected_phone,
                'password': expected_password,
            },
        )


@pytest.mark.parametrize(argnames=SET_PASSWORD_ARGNAMES, argvalues=SET_PASSWORD_ARGVALUES)
@pytest.mark.django_db
def test_password_updated(
    user_service: BaseUserService,
    user: User,
    expected_password: str,
):
    """Test that the password is updated successfully"""
    assert user.check_password(expected_password) is False
    user_service.set_password(user=user, password=expected_password)
    assert user.check_password(expected_password) is True
