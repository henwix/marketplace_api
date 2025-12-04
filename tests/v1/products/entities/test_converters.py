import pytest

from src.apps.users.converters import user_from_entity, user_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.models import User


@pytest.mark.django_db
def test_user_converted_to_entity(user: User):
    converted_entity = user_to_entity(dto=user)

    assert isinstance(converted_entity, UserEntity)
    assert converted_entity.id == user.pk
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
def test_user_converted_from_entity(user: User):
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
