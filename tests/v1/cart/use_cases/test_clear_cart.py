import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.cart.commands import ClearCartCommand
from src.apps.cart.exceptions import CartEmptyError
from src.apps.cart.models import Cart, CartItem
from src.apps.cart.use_cases.clear_cart import ClearCartUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from tests.v1.cart.factories import CartItemModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def clear_cart_use_case(container: Container) -> ClearCartUseCase:
    return container.resolve(ClearCartUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize('expected_items_count', [1, 4, 6, 10, 20, 25, 29, 35, 43, 48, 50])
def test_clear_cart_data_cleared(clear_cart_use_case: ClearCartUseCase, cart: Cart, expected_items_count: int):
    CartItemModelFactory.create_batch(size=expected_items_count, cart=cart)
    assert CartItem.objects.filter(cart_id=cart.id).count() == expected_items_count
    command = ClearCartCommand(user_id=cart.user_id)
    clear_cart_use_case.execute(command=command)
    assert CartItem.objects.filter(cart_id=cart.id).count() == 0


@pytest.mark.django_db
def test_clear_cart_empty_cart_error_raised(clear_cart_use_case: ClearCartUseCase, cart: Cart):
    with pytest.raises(CartEmptyError):
        command = ClearCartCommand(user_id=cart.user_id)
        clear_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_clear_cart_credentials_error_raised(clear_cart_use_case: ClearCartUseCase):
    command = ClearCartCommand(user_id=None)
    with pytest.raises(AuthCredentialsNotProvidedError):
        clear_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_clear_cart_user_not_found_error_raised(clear_cart_use_case: ClearCartUseCase):
    command = ClearCartCommand(user_id=1)
    with pytest.raises(UserNotFoundError):
        clear_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_clear_cart_user_not_active_error_raised(clear_cart_use_case: ClearCartUseCase):
    user = UserModelFactory.create(is_active=False)
    command = ClearCartCommand(user_id=user.pk)
    with pytest.raises(UserNotActiveError):
        clear_cart_use_case.execute(command=command)
