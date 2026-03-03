import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.cart.commands import GetCartCommand
from src.apps.cart.converters import cart_item_to_entity
from src.apps.cart.exceptions import CartEmptyError
from src.apps.cart.models import Cart, CartItem
from src.apps.cart.use_cases.get_cart import GetCartUseCase
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from tests.v1.cart.factories import CartItemModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def get_cart_use_case(container: Container) -> GetCartUseCase:
    return container.resolve(GetCartUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize('expected_items_count', [1, 4, 6, 10, 20, 25, 29, 35, 43, 48, 50])
def test_get_cart_returns_correct_data(
    get_cart_use_case: GetCartUseCase, cart: Cart, seller: Seller, expected_items_count: int
):
    CartItemModelFactory.create_batch(size=expected_items_count, cart=cart, seller=seller)
    db_items = CartItem.objects.filter(cart_id=cart.id).order_by('-created_at')
    expected_cart_price = sum([item.price_snapshot * item.quantity for item in db_items])
    expected_items = [cart_item_to_entity(dto=item) for item in db_items]

    command = GetCartCommand(user_id=cart.user_id)
    retreived_items, retrieved_cart_price, retrieved_items_count = get_cart_use_case.execute(command=command)
    assert retreived_items == expected_items
    assert retrieved_cart_price == expected_cart_price
    assert retrieved_items_count == expected_items_count


@pytest.mark.django_db
def test_get_cart_empty_cart_error_raised_if_not_cart_items(get_cart_use_case: GetCartUseCase, cart: Cart):
    with pytest.raises(CartEmptyError):
        command = GetCartCommand(user_id=cart.user_id)
        get_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_cart_credentials_error_raised(get_cart_use_case: GetCartUseCase):
    command = GetCartCommand(user_id=None)
    with pytest.raises(AuthCredentialsNotProvidedError):
        get_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_cart_user_not_found_error_raised(get_cart_use_case: GetCartUseCase):
    command = GetCartCommand(user_id=1)
    with pytest.raises(UserNotFoundError):
        get_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_cart_user_not_active_error_raised(get_cart_use_case: GetCartUseCase):
    user = UserModelFactory.create(is_active=False)
    command = GetCartCommand(user_id=user.pk)
    with pytest.raises(UserNotActiveError):
        get_cart_use_case.execute(command=command)
