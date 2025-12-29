import pytest

from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from src.apps.users.converters import data_to_user_entity, user_from_entity, user_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.models import User


def test_convert_data_to_user_entity():
    data = {
        'first_name': 'test first_name',
        'last_name': 'test last_name',
        'phone': '+55555555555',
        'email': 'test_email@example.com',
    }
    converted_entity = data_to_user_entity(data=data)

    assert isinstance(converted_entity, UserEntity)
    assert converted_entity.id is None
    assert converted_entity.seller_profile is None
    assert converted_entity.first_name == data['first_name']
    assert converted_entity.last_name == data['last_name']
    assert converted_entity.email == data['email']
    assert converted_entity.phone == data['phone']
    assert converted_entity.password is None
    assert converted_entity.avatar is None
    assert converted_entity.is_staff is False
    assert converted_entity.is_active is True
    assert converted_entity.date_joined is None


@pytest.mark.django_db
def test_convert_user_to_entity(seller: Seller):
    user = User.objects.select_related('seller_profile').get(pk=seller.user_id)
    converted_entity = user_to_entity(dto=user)

    assert isinstance(converted_entity, UserEntity)
    assert converted_entity.id == user.pk
    assert converted_entity.seller_profile == seller_to_entity(dto=user.seller_profile)
    assert converted_entity.first_name == user.first_name
    assert converted_entity.last_name == user.last_name
    assert converted_entity.email == user.email
    assert converted_entity.phone == user.phone
    assert converted_entity.password == user.password
    assert converted_entity.avatar == user.avatar
    assert converted_entity.is_staff == user.is_staff
    assert converted_entity.is_active == user.is_active
    assert converted_entity.date_joined == user.date_joined


@pytest.mark.django_db
def test_convert_user_from_entity(user: User):
    converted_entity = user_to_entity(dto=user)
    converted_user = user_from_entity(entity=converted_entity)

    assert isinstance(converted_user, User)
    assert converted_user.pk == user.pk
    assert converted_user.first_name == user.first_name
    assert converted_user.last_name == user.last_name
    assert converted_user.email == user.email
    assert converted_user.phone == user.phone
    assert converted_user.password == user.password
    assert converted_user.avatar == user.avatar
    assert converted_user.is_staff == user.is_staff
    assert converted_user.is_active == user.is_active
    assert converted_user.date_joined == user.date_joined
