import pytest

from src.apps.sellers.converters.sellers import seller_from_entity, seller_to_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.models import Seller


@pytest.mark.django_db
def test_convert_seller_to_entity(seller: Seller):
    converted_entity = seller_to_entity(dto=seller)

    assert isinstance(converted_entity, SellerEntity)
    assert converted_entity.id == seller.pk
    assert converted_entity.user_id == seller.user_id
    assert converted_entity.name == seller.name
    assert converted_entity.description == seller.description
    assert converted_entity.avatar == seller.avatar
    assert converted_entity.background == seller.background
    assert converted_entity.created_at == seller.created_at
    assert converted_entity.updated_at == seller.updated_at


@pytest.mark.django_db
def test_convert_seller_from_entity(seller: Seller):
    converted_entity = seller_to_entity(dto=seller)
    converted_seller = seller_from_entity(entity=converted_entity)

    assert isinstance(converted_seller, Seller)
    assert converted_seller.id == seller.pk
    assert converted_seller.user_id == seller.user_id
    assert converted_seller.name == seller.name
    assert converted_seller.description == seller.description
    assert converted_seller.avatar == seller.avatar
    assert converted_seller.background == seller.background
    assert converted_seller.created_at == seller.created_at
    assert converted_seller.updated_at == seller.updated_at
