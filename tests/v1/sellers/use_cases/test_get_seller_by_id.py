import pytest
from punq import Container

from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.exceptions import SellerNotFoundByIdError
from src.apps.sellers.models import Seller
from src.apps.sellers.use_cases.get_by_id import GetSellerByIdUseCase


@pytest.fixture
def get_seller_by_id_use_case(container: Container) -> GetSellerByIdUseCase:
    return container.resolve(GetSellerByIdUseCase)


@pytest.mark.django_db
def test_get_seller_by_id_retrieved(get_seller_by_id_use_case: GetSellerByIdUseCase, seller: Seller):
    retrieved_seller = get_seller_by_id_use_case.execute(seller_id=seller.pk)
    assert isinstance(retrieved_seller, SellerEntity)
    assert seller_to_entity(dto=seller) == retrieved_seller


@pytest.mark.django_db
def test_get_seller_by_id_not_found_error_raised_if_not_exists(get_seller_by_id_use_case: GetSellerByIdUseCase):
    with pytest.raises(SellerNotFoundByIdError):
        get_seller_by_id_use_case.execute(seller_id=1)
