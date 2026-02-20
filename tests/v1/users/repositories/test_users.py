import pytest
from django.core.exceptions import ValidationError

from src.apps.sellers.models import Seller
from src.apps.users.converters import user_from_entity, user_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.models import User
from src.apps.users.repositories.users import BaseUserRepository
from tests.v1.users.factories import UserModelFactory
from tests.v1.users.test_data.create_user import (
    CREATE_USER_ARGNAMES,
    CREATE_USER_ARGVALUES,
    CREATE_USER_WITH_NONE_ARGVALUES,
)
from tests.v1.users.test_data.set_password_user import SET_PASSWORD_ARGNAMES, SET_PASSWORD_ARGVALUES


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_create_user_created(
    user_repository: BaseUserRepository,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    """Test that a user is created successfully"""
    created_user = user_repository.create(
        first_name=expected_first_name,
        last_name=expected_last_name,
        email=expected_email,
        phone=expected_phone,
        password=expected_password,
    )

    assert isinstance(created_user, UserEntity)
    assert created_user.first_name == expected_first_name
    assert created_user.last_name == expected_last_name
    assert created_user.email == expected_email
    assert created_user.phone == expected_phone
    assert created_user.seller_profile is None
    assert created_user.avatar is None
    assert created_user.is_staff is False
    assert created_user.is_active is True
    assert user_from_entity(entity=created_user).check_password(expected_password) is True


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_WITH_NONE_ARGVALUES)
def test_create_user_validation_error_raised(
    user_repository: BaseUserRepository,
    expected_first_name: str | None,
    expected_last_name: str | None,
    expected_email: str | None,
    expected_phone: str | None,
    expected_password: str,
):
    """Test that creating a user without required fields raises a validation error"""
    with pytest.raises(ValidationError):
        user_repository.create(
            first_name=expected_first_name,
            last_name=expected_last_name,
            email=expected_email,
            phone=expected_phone,
            password=expected_password,
        )


@pytest.mark.parametrize(argnames=SET_PASSWORD_ARGNAMES, argvalues=SET_PASSWORD_ARGVALUES)
@pytest.mark.django_db
def test_update_password_updated(
    user_repository: BaseUserRepository,
    user: User,
    expected_password: str,
):
    """Test that the password is updated successfully"""
    assert user.check_password(expected_password) is False
    user_repository.set_password(user=user_to_entity(dto=user), password=expected_password)
    user.refresh_from_db()
    assert user.check_password(expected_password) is True


@pytest.mark.django_db
def test_get_user_by_id_retrieved(user_repository: BaseUserRepository, user: User):
    retrieved_user = user_repository.get_by_id(id=user.pk)
    assert isinstance(retrieved_user, User)
    assert retrieved_user == user


@pytest.mark.django_db
def test_get_user_by_id_not_retrieved_if_not_exists(user_repository: BaseUserRepository, user: User):
    assert user_repository.get_by_id(id=1) is None


@pytest.mark.django_db
def test_get_user_with_loaded_seller_by_id_retrieved(user_repository: BaseUserRepository, seller: Seller):
    retrieved_user = user_repository.get_by_id_with_loaded_seller(id=seller.user_id)
    assert isinstance(retrieved_user, User)
    assert retrieved_user == seller.user
    assert retrieved_user._state.fields_cache.get('seller_profile') == seller


@pytest.mark.django_db
def test_get_user_with_loaded_seller_by_id_not_retrieved_if_not_exists(user_repository: BaseUserRepository):
    assert user_repository.get_by_id_with_loaded_seller(id=1) is None


@pytest.mark.django_db
def test_delete_user_deleted(user_repository: BaseUserRepository, user: User):
    assert User.objects.filter(pk=user.pk).exists()
    user_repository.delete(id=user.pk)
    assert not User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_save_user_saved_for_creation(user_repository: BaseUserRepository):
    user = UserModelFactory.build()
    assert not User.objects.filter(pk=user.pk).exists()
    saved_user = user_repository.save(user=user_to_entity(dto=user), update=False)
    assert isinstance(saved_user, UserEntity)
    db_user = User.objects.get(pk=saved_user.id)
    assert db_user.first_name == saved_user.first_name
    assert db_user.last_name == saved_user.last_name
    assert db_user.email == saved_user.email
    assert db_user.phone == saved_user.phone


@pytest.mark.django_db
def test_save_user_saved_for_update(user_repository: BaseUserRepository, user: User):
    user.first_name = 'new test first name'
    user.last_name = 'new test last name'
    user.email = 'newtestemail@test.com'
    user.phone = '+129125575125125'

    saved_user = user_repository.save(user=user_to_entity(dto=user), update=True)
    assert isinstance(saved_user, UserEntity)
    db_user = User.objects.get(pk=user.pk)
    assert db_user.first_name == saved_user.first_name
    assert db_user.last_name == saved_user.last_name
    assert db_user.email == saved_user.email
    assert db_user.phone == saved_user.phone
