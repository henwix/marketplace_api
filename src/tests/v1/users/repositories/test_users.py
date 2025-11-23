import pytest

from src.apps.users.models import User
from src.apps.users.repositories.users import BaseUserRepository


@pytest.mark.parametrize(
    argnames=[
        'expected_first_name',
        'expected_last_name',
        'expected_email',
        'expected_phone',
        'expected_password',
    ],
    argvalues=[
        ('Hello', 'World', 'test@example.com', '+978658358284', 'test_password_123456'),
        ('John', 'Doe', 'john@example.com', '+18482612425', 'johndoe82461942'),
        ('Jane', 'Doe', 'JaneDoe@test.com', '+1234567690249238', 'JANE_DOE_PASSWORD-1029!@)$&0217501231'),
        ('Name', 'Test', 'HelloWorld@test.test', '+887674726472112', 'helloworld_1234+_()*#@!@(&$%)(*!@&^%!^$%(@!($)'),
    ],
)
@pytest.mark.django_db
def test_user_created(
    user_repository: BaseUserRepository,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    created_user = user_repository.create(
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


@pytest.mark.parametrize(
    'expected_password',
    ['1234q1234q', '9124972ASkjfhakjfgLF', 'HelloWorld_41528', 'Gjaskjdh12h', 'new_password_test_12391724_TEST'],
)
@pytest.mark.django_db
def test_password_updated(
    user_repository: BaseUserRepository,
    user: User,
    expected_password: str,
):
    assert not user.check_password(expected_password)
    user_repository.set_password(user=user, password=expected_password)
    assert user.check_password(expected_password)
