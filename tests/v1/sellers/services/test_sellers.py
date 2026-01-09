import pytest
from punq import Container

from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.services.sellers import BaseSellerService
from src.apps.users.models import User
from tests.v1.sellers.test_data.create_seller import CREATE_SELLER_ARGNAMES, CREATE_SELLER_ARGVALUES


@pytest.fixture
def seller_service(container: Container) -> BaseSellerService:
    return container.resolve(BaseSellerService)


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_create_seller_created(
    seller_service: BaseSellerService,
    user: User,
    expected_name: str,
    expected_description: str,
):
    entity = SellerEntity.create(
        name=expected_name,
        description=expected_description,
        user_id=user.pk,
    )
    seller = seller_service.save(seller=entity)
    assert isinstance(seller, SellerEntity)
    assert seller.user_id == user.pk
    assert seller.name == expected_name
    assert seller.description == expected_description
    assert seller.avatar is None
    assert seller.background is None
