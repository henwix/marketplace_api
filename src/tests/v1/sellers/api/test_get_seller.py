import pytest
from rest_framework import status

from src.apps.sellers.models import Seller
from src.apps.users.models import User
from src.tests.v1.conftest import get_client


@pytest.mark.django_db
def test_seller_retrieved(seller: Seller):
    client = get_client(user=seller.user, jwt=True)

    response = client.get(path='/v1/sellers/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('id') == seller.pk
    assert response.data.get('name') == seller.name
    assert response.data.get('description') == seller.description
    assert response.data.get('avatar') is None
    assert response.data.get('background') is None


@pytest.mark.django_db
def test_seller_not_retrieved_and_returns_401_if_unauthorized():
    client = get_client()
    response = client.get(path='/v1/sellers/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_seller_not_retrieved_and_returns_403_if_does_not_exist(user: User):
    client = get_client(user=user, jwt=True)
    response = client.get(path='/v1/sellers/')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not Seller.objects.filter(user_id=user.pk).exists()
