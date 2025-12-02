import punq
import pytest

from src.apps.sellers.use_cases.create import CreateSellerUseCase
from src.apps.users.models import User
from tests.v1.sellers.test_data.create_seller import CREATE_SELLER_ARGNAMES, CREATE_SELLER_ARGVALUES


@pytest.fixture
def create_seller_use_case(container: punq.Container) -> CreateSellerUseCase:
    return container.resolve(CreateSellerUseCase)


@pytest.mark.parametrize(argnames=CREATE_SELLER_ARGNAMES, argvalues=CREATE_SELLER_ARGVALUES)
@pytest.mark.django_db
def test_seller_created(
    create_seller_use_case: CreateSellerUseCase,
    user: User,
    expected_name: str,
    expected_description: str,
):
    expected_seller_data = {
        'name': expected_name,
        'description': expected_description,
    }

    seller = create_seller_use_case.execute(user_id=user.pk, data=expected_seller_data)
    assert seller.user_id == user.pk
    assert seller.name == expected_name
    assert seller.description == expected_description
    assert seller.avatar is None
    assert seller.background is None
