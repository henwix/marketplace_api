import pytest
from rest_framework import status

from src.apps.sellers.models import Seller
from src.apps.users.models import User
from tests.v1.conftest import get_client


@pytest.mark.django_db
def test_delete_seller_deleted(seller: Seller):
    user = seller.user
    client = get_client(user=user, jwt=True)

    assert Seller.objects.filter(user_id=user.pk).exists()
    response = client.delete(path='/v1/sellers/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Seller.objects.filter(user_id=user.pk).exists()


@pytest.mark.django_db
def test_delete_seller_not_deleted_and_returns_401_if_unauthorized():
    client = get_client()
    response = client.delete(path='/v1/sellers/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_seller_not_deleted_and_returns_404_if_does_not_exist(user: User):
    client = get_client(user=user, jwt=True)
    response = client.delete(path='/v1/sellers/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert not Seller.objects.filter(user_id=user.pk).exists()
