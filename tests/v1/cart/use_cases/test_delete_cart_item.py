from uuid import uuid7

import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.cart.commands import DeleteCartItemCommand
from src.apps.cart.exceptions import ItemNotFoundInCartError
from src.apps.cart.models import CartItem
from src.apps.cart.use_cases.delete_cart_item import DeleteCartItemUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def delete_cart_item_use_case(container: Container) -> DeleteCartItemUseCase:
    return container.resolve(DeleteCartItemUseCase)


@pytest.mark.django_db
def test_delete_cart_item_deleted(delete_cart_item_use_case: DeleteCartItemUseCase, cart_item: CartItem):
    assert CartItem.objects.filter(pk=cart_item.id).exists()
    command = DeleteCartItemCommand(user_id=cart_item.cart.user_id, product_variant_id=cart_item.product_variant_id)
    delete_cart_item_use_case.execute(command=command)
    assert not CartItem.objects.filter(pk=cart_item.id).exists()


@pytest.mark.django_db
def test_delete_cart_item_not_deleted_and_item_not_found_in_cart_error_raised(
    delete_cart_item_use_case: DeleteCartItemUseCase, user: User
):
    with pytest.raises(ItemNotFoundInCartError):
        command = DeleteCartItemCommand(user_id=user.id, product_variant_id=uuid7())
        delete_cart_item_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_cart_item_credentials_error_raised(delete_cart_item_use_case: DeleteCartItemUseCase):
    command = DeleteCartItemCommand(user_id=None, product_variant_id=uuid7())
    with pytest.raises(AuthCredentialsNotProvidedError):
        delete_cart_item_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_cart_item_user_not_found_error_raised(delete_cart_item_use_case: DeleteCartItemUseCase):
    command = DeleteCartItemCommand(user_id=1, product_variant_id=uuid7())
    with pytest.raises(UserNotFoundError):
        delete_cart_item_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_cart_item_user_not_active_error_raised(delete_cart_item_use_case: DeleteCartItemUseCase):
    user = UserModelFactory.create(is_active=False)
    command = DeleteCartItemCommand(user_id=user.pk, product_variant_id=uuid7())
    with pytest.raises(UserNotActiveError):
        delete_cart_item_use_case.execute(command=command)
