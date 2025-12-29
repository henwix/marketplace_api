import pytest
from rest_framework import status

from src.apps.sellers.models import Seller
from src.apps.users.models import User
from tests.v1.conftest import get_client
from tests.v1.sellers.test_data.create_seller import CREATE_SELLER_ARGNAMES, CREATE_SELLER_ARGVALUES


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_create_seller_created(
    user: User,
    expected_name: str,
    expected_description: str,
):
    client = get_client(user=user, jwt=True)
    expected_seller_data = {'name': expected_name, 'description': expected_description}

    response = client.post(path='/v1/sellers/', data=expected_seller_data)
    seller = Seller.objects.get(user_id=user.pk)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data.get('id') == seller.pk
    assert seller.name == expected_name
    assert seller.description == expected_description
    assert response.data.get('name') == expected_name
    assert response.data.get('description') == expected_description
    assert response.data.get('avatar') is None
    assert response.data.get('background') is None


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_create_seller_not_created_and_returns_401_if_unauthorized(
    expected_name: str,
    expected_description: str,
):
    client = get_client()
    expected_seller_data = {'name': expected_name, 'description': expected_description}

    response = client.post(path='/v1/sellers/', data=expected_seller_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_create_seller_not_created_and_returns_400_if_already_exists(
    seller: Seller,
    expected_name: str,
    expected_description: str,
):
    client = get_client(user=seller.user, jwt=True)
    expected_seller_data = {'name': expected_name, 'description': expected_description}

    response = client.post(path='/v1/sellers/', data=expected_seller_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
