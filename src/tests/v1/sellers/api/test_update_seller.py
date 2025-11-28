import pytest
from rest_framework import status

from src.apps.sellers.models import Seller
from src.apps.users.models import User
from src.tests.v1.conftest import get_client
from src.tests.v1.sellers.test_data.create_seller import CREATE_SELLER_ARGNAMES, CREATE_SELLER_ARGVALUES


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_seller_updated_put(
    seller: Seller,
    expected_name: str,
    expected_description: str,
):
    user = seller.user
    client = get_client(user=user, jwt=True)
    expected_seller_data = {'name': expected_name, 'description': expected_description}

    response = client.put(path='/v1/sellers/', data=expected_seller_data)
    db_seller = Seller.objects.get(user_id=user.pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('id') == db_seller.pk
    assert db_seller.name == expected_name
    assert db_seller.description == expected_description
    assert response.data.get('name') == expected_name
    assert response.data.get('description') == expected_description
    assert response.data.get('avatar') is None
    assert response.data.get('background') is None


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_seller_updated_patch(
    seller: Seller,
    expected_name: str,
    expected_description: str,
):
    user = seller.user
    client = get_client(user=user, jwt=True)
    expected_seller_data = {'name': expected_name, 'description': expected_description}

    response = client.patch(path='/v1/sellers/', data=expected_seller_data)
    db_seller = Seller.objects.get(user_id=user.pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('id') == db_seller.pk
    assert db_seller.name == expected_name
    assert db_seller.description == expected_description
    assert response.data.get('name') == expected_name
    assert response.data.get('description') == expected_description
    assert response.data.get('avatar') is None
    assert response.data.get('background') is None


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_seller_not_updated_and_returns_401_if_unauthorized_put(
    expected_name: str,
    expected_description: str,
):
    client = get_client()
    expected_seller_data = {'name': expected_name, 'description': expected_description}

    response = client.put(path='/v1/sellers/', data=expected_seller_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_seller_not_updated_and_returns_401_if_unauthorized_patch(
    expected_name: str,
    expected_description: str,
):
    client = get_client()
    expected_seller_data = {'name': expected_name, 'description': expected_description}

    response = client.patch(path='/v1/sellers/', data=expected_seller_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_seller_not_updated_and_returns_403_if_does_not_exist_put(
    user: User,
    expected_name: str,
    expected_description: str,
):
    client = get_client(user=user, jwt=True)
    expected_seller_data = {'name': expected_name, 'description': expected_description}

    response = client.put(path='/v1/sellers/', data=expected_seller_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_seller_not_updated_and_returns_403_if_does_not_exist_patch(
    user: User,
    expected_name: str,
    expected_description: str,
):
    client = get_client(user=user, jwt=True)
    expected_seller_data = {'name': expected_name, 'description': expected_description}

    response = client.patch(path='/v1/sellers/', data=expected_seller_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
