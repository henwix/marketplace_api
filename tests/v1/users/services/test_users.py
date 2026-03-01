import pytest

from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from src.apps.users.converters import user_from_entity, user_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError, UserWithDataAlreadyExistsError
from src.apps.users.models import User
from src.apps.users.services.users import BaseUserService
from tests.v1.users.factories import UserModelFactory
from tests.v1.users.test_data.create_user import CREATE_USER_ARGNAMES, CREATE_USER_ARGVALUES
from tests.v1.users.test_data.set_password_user import SET_PASSWORD_ARGNAMES, SET_PASSWORD_ARGVALUES


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_create_user_created(
    user_service: BaseUserService,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    """Test that a user is created successfully"""
    created_user = user_service.create(
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
    assert user_from_entity(entity=created_user).check_password(expected_password) is True


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_create_user_not_created_and_email_already_exists_error_raised(
    user_service: BaseUserService,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    """Test that creating a user with an existing email raises an error"""
    UserModelFactory.create(email=expected_email)

    with pytest.raises(UserWithDataAlreadyExistsError):
        user_service.create(
            first_name=expected_first_name,
            last_name=expected_last_name,
            email=expected_email,
            phone=expected_phone,
            password=expected_password,
        )


@pytest.mark.parametrize(argnames=CREATE_USER_ARGNAMES, argvalues=CREATE_USER_ARGVALUES)
@pytest.mark.django_db
def test_create_user_not_created_and_phone_already_exists_error_raised(
    user_service: BaseUserService,
    expected_first_name: str,
    expected_last_name: str,
    expected_email: str,
    expected_phone: str,
    expected_password: str,
):
    """Test that creating a user with an existing phone raises an error"""
    UserModelFactory.create(phone=expected_phone)

    with pytest.raises(UserWithDataAlreadyExistsError):
        user_service.create(
            first_name=expected_first_name,
            last_name=expected_last_name,
            email=expected_email,
            phone=expected_phone,
            password=expected_password,
        )


@pytest.mark.django_db
def test_get_user_by_id_retrieved(user_service: BaseUserService, user: User):
    retrieved_user = user_service.try_get_active_by_id(id=user.pk)
    assert isinstance(retrieved_user, UserEntity)
    assert retrieved_user == user_to_entity(dto=user)


@pytest.mark.django_db
def test_get_user_by_id_not_retrieved_if_not_exists_and_not_found_error_raised(user_service: BaseUserService):
    with pytest.raises(UserNotFoundError):
        user_service.try_get_active_by_id(id=1)


@pytest.mark.django_db
def test_get_user_by_id_not_retrieved_if_not_active_and_not_active_error_raised(user_service: BaseUserService):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        user_service.try_get_active_by_id(id=user.pk)


@pytest.mark.django_db
def test_get_user_with_loaded_seller_by_id_retrieved(user_service: BaseUserService, seller: Seller):
    retrieved_user = user_service.try_get_by_id_with_loaded_seller(id=seller.user_id)
    assert isinstance(retrieved_user, UserEntity)
    assert retrieved_user.id == seller.user.id
    assert retrieved_user.first_name == seller.user.first_name
    assert retrieved_user.last_name == seller.user.last_name
    assert retrieved_user.email == seller.user.email
    assert retrieved_user.phone == seller.user.phone
    assert retrieved_user.avatar == seller.user.avatar
    assert retrieved_user.is_staff == seller.user.is_staff
    assert retrieved_user.is_active == seller.user.is_active
    assert retrieved_user.date_joined == seller.user.date_joined
    assert retrieved_user.seller_profile == seller_to_entity(dto=seller)


@pytest.mark.django_db
def test_get_user_with_loaded_seller_by_id_not_retrieved_if_not_exists_and_not_found_error_raised(
    user_service: BaseUserService,
):
    with pytest.raises(UserNotFoundError):
        user_service.try_get_by_id_with_loaded_seller(id=1)


@pytest.mark.django_db
def test_get_user_with_loaded_seller_by_id_not_retrieved_if_not_active_and_not_active_error_raised(
    user_service: BaseUserService,
):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        user_service.try_get_by_id_with_loaded_seller(id=user.pk)


@pytest.mark.parametrize(argnames=SET_PASSWORD_ARGNAMES, argvalues=SET_PASSWORD_ARGVALUES)
@pytest.mark.django_db
def test_update_user_password_updated(
    user_service: BaseUserService,
    user: User,
    expected_password: str,
):
    """Test that the password is updated successfully"""
    assert user.check_password(expected_password) is False
    user_service.set_password(user=user_to_entity(dto=user), password=expected_password)

    db_user = User.objects.get(pk=user.pk)
    assert db_user.check_password(expected_password) is True


@pytest.mark.django_db
def test_delete_user_deleted(user_service: BaseUserService, user: User):
    assert User.objects.filter(pk=user.pk).exists()
    user_service.delete(id=user.pk)
    assert not User.objects.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_save_user_saved_for_creation(user_service: BaseUserService):
    user = UserModelFactory.build()
    assert not User.objects.filter(pk=user.pk).exists()
    saved_user = user_service.save(user=user_to_entity(dto=user), update=False)
    assert isinstance(saved_user, UserEntity)
    db_user = User.objects.get(pk=saved_user.id)
    assert user_to_entity(db_user) == saved_user


@pytest.mark.django_db
def test_save_user_saved_for_update(user_service: BaseUserService, user: User):
    user.first_name = 'new test first name'
    user.last_name = 'new test last name'
    user.email = 'newtestemail@test.com'
    user.phone = '+129125575125125'

    saved_user = user_service.save(user=user_to_entity(dto=user), update=True)
    assert isinstance(saved_user, UserEntity)
    db_user = User.objects.get(pk=user.pk)
    assert user_to_entity(dto=db_user) == saved_user


@pytest.mark.django_db
def test_save_user_not_saved_and_data_already_exists_error_raised(user_service: BaseUserService, user: User):
    new_user = UserModelFactory.create()
    new_user.phone = user.phone
    new_user.email = user.email
    with pytest.raises(UserWithDataAlreadyExistsError):
        user_service.save(user=user_to_entity(dto=new_user))
