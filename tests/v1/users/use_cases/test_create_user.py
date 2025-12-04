import punq
import pytest

from src.apps.users.converters import user_from_entity
from src.apps.users.entities import UserEntity
from src.apps.users.use_cases.create import CreateUserUseCase
from tests.v1.users.test_data.create_user import CREATE_USER_ARGNAMES, CREATE_USER_ARGVALUES


@pytest.fixture
def create_user_use_case(container: punq.Container) -> CreateUserUseCase:
    return container.resolve(CreateUserUseCase)


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_user_created(
    create_user_use_case: CreateUserUseCase,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    """Test that a user is created successfully"""
    created_user = create_user_use_case.execute(
        data={
            'first_name': expected_first_name,
            'last_name': expected_last_name,
            'email': expected_email,
            'phone': expected_phone,
            'password': expected_password,
        },
    )

    assert isinstance(created_user, UserEntity)
    assert created_user.first_name == expected_first_name
    assert created_user.last_name == expected_last_name
    assert created_user.email == expected_email
    assert created_user.phone == expected_phone
    assert user_from_entity(entity=created_user).check_password(expected_password) is True
