import pytest
from rest_framework import status

from src.apps.users.models import User
from tests.v1.conftest import get_client
from tests.v1.users.factories import UserModelFactory
from tests.v1.users.test_data.create_user import CREATE_USER_ARGNAMES, CREATE_USER_ARGVALUES


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_user_created(
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    client = get_client()
    expected_user_data = {
        'first_name': expected_first_name,
        'last_name': expected_last_name,
        'email': expected_email,
        'phone': expected_phone,
        'password': expected_password,
    }

    response = client.post(path='/v1/users/', data=expected_user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.data.get('id'), int)
    assert response.data.get('first_name') == expected_first_name
    assert response.data.get('last_name') == expected_last_name
    assert response.data.get('email') == expected_email
    assert response.data.get('phone') == expected_phone
    assert response.data.get('avatar') is None


@pytest.mark.django_db
def test_user_created_with_phone_equals_none():
    UserModelFactory.create(phone=None)

    expected_first_name = 'Alex'
    expected_last_name = 'Johnson'
    expected_email = 'alex@example.com'
    expected_phone = None
    client = get_client()
    expected_user_data = {
        'first_name': expected_first_name,
        'last_name': expected_last_name,
        'email': expected_email,
        'phone': None,
        'password': '1234q1234q',
    }

    response = client.post(path='/v1/users/', data=expected_user_data, content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.data.get('id'), int)
    assert response.data.get('first_name') == expected_first_name
    assert response.data.get('last_name') == expected_last_name
    assert response.data.get('email') == expected_email
    assert response.data.get('phone') is expected_phone
    assert response.data.get('avatar') is None


@pytest.mark.django_db
def test_user_not_created_and_returns_400_if_email_already_exists(user: User):
    client = get_client()
    expected_user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': '+99999999999',
        'password': 'test_user_password_123456',
    }

    response = client.post(path='/v1/users/', data=expected_user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'User with this email already exists' == response.data.get('detail')


@pytest.mark.django_db
def test_user_not_created_and_returns_400_if_phone_already_exists():
    user = UserModelFactory.create(phone='+9999999999')
    client = get_client()
    expected_user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': 'test@test.com',
        'phone': user.phone,
        'password': 'test_user_password_123456',
    }

    response = client.post(path='/v1/users/', data=expected_user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'User with this phone already exists' == response.data.get('detail')


@pytest.mark.django_db
def test_user_not_created_and_returns_400_if_password_invalid():
    client = get_client()
    expected_user_data = {'password': '1'}

    response = client.post(path='/v1/users/', data=expected_user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'This password is too short. It must contain at least 8 characters.' in response.data.get('password')
    assert 'This password is too common.' in response.data.get('password')
    assert 'This password is entirely numeric.' in response.data.get('password')
