import pytest
from punq import Container

from src.apps.sellers.converters.sellers import data_to_seller_entity, seller_from_entity
from src.apps.sellers.models import Seller
from src.apps.sellers.repositories.sellers import BaseSellerRepository
from src.apps.users.models import User
from tests.v1.sellers.test_data.create_seller import CREATE_SELLER_ARGNAMES, CREATE_SELLER_ARGVALUES


@pytest.fixture
def seller_repository(container: Container) -> BaseSellerRepository:
    return container.resolve(BaseSellerRepository)


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_create_seller_created(
    seller_repository: BaseSellerRepository,
    user: User,
    expected_name: str,
    expected_description: str,
):
    expected_seller_data = {
        'user_id': user.pk,
        'name': expected_name,
        'description': expected_description,
    }

    seller = seller_repository.save(
        seller=seller_from_entity(data_to_seller_entity(data=expected_seller_data)), update=False
    )
    assert isinstance(seller, Seller)
    assert seller.user_id == user.pk
    assert seller.name == expected_name
    assert seller.description == expected_description
    assert seller.avatar is None
    assert seller.background is None
