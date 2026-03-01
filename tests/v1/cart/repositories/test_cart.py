from decimal import Decimal

import pytest

from src.apps.cart.converters import cart_item_to_entity, cart_to_entity
from src.apps.cart.entities import CartEntity
from src.apps.cart.models import Cart, CartItem
from src.apps.cart.repositories.cart import BaseCartRepository
from src.apps.products.models.product_variants import ProductVariant
from src.apps.sellers.models import Seller
from src.apps.users.models import User
from tests.v1.cart.factories import CartItemModelFactory


@pytest.mark.django_db
def test_get_or_create_cart_returns_existing_cart(cart_repository: BaseCartRepository, cart: Cart):
    assert Cart.objects.filter(user_id=cart.user_id).exists()
    retrieved_cart = cart_repository.get_or_create_cart_for_update(user_id=cart.user_id)
    assert isinstance(retrieved_cart, CartEntity)
    assert cart_to_entity(dto=cart) == retrieved_cart


@pytest.mark.django_db
def test_get_or_create_cart_creates_cart_when_not_exists(cart_repository: BaseCartRepository, user: User):
    assert not Cart.objects.filter(user_id=user.id).exists()
    created_cart = cart_repository.get_or_create_cart_for_update(user_id=user.id)
    db_cart = Cart.objects.get(user_id=user.id)
    assert created_cart == cart_to_entity(dto=db_cart)


@pytest.mark.django_db
@pytest.mark.parametrize('expected_items_count', [1, 4, 6, 10, 20, 25, 29, 35, 43, 48, 50])
def test_get_cart_items_by_cart_id_returns_items(
    cart_repository: BaseCartRepository, cart: Cart, expected_items_count: int, seller: Seller
):
    CartItemModelFactory.create_batch(expected_items_count, cart=cart, seller=seller)
    retrieved_cart_items = cart_repository.get_cart_items_by_cart_id(cart_id=cart.id)
    db_cart_items = CartItem.objects.filter(cart_id=cart.id).order_by('-created_at')
    assert isinstance(retrieved_cart_items, list)
    assert len(retrieved_cart_items) == expected_items_count
    for retrieved_item, db_item in zip(retrieved_cart_items, db_cart_items, strict=True):
        assert retrieved_item == cart_item_to_entity(dto=db_item)


@pytest.mark.django_db
def test_get_cart_items_by_cart_id_returns_empty_list_if_no_items(cart_repository: BaseCartRepository, cart: Cart):
    retrieved_cart_items = cart_repository.get_cart_items_by_cart_id(cart_id=cart.id)
    assert isinstance(retrieved_cart_items, list)
    assert len(retrieved_cart_items) == 0


@pytest.mark.django_db
@pytest.mark.parametrize('expected_items_count', [1, 4, 6, 10, 20, 25, 29, 35, 43, 48, 50])
def test_get_total_cart_price_returns_price_of_items(
    cart_repository: BaseCartRepository, cart: Cart, seller: Seller, expected_items_count: int
):
    cart_items = CartItemModelFactory.create_batch(size=expected_items_count, cart=cart, seller=seller)
    expected_cart_price = sum([item.price_snapshot * item.quantity for item in cart_items])
    assert cart_repository.get_total_cart_price(cart_id=cart.id) == expected_cart_price


@pytest.mark.django_db
def test_get_total_cart_price_returns_zero_if_no_items(cart_repository: BaseCartRepository, cart: Cart):
    assert cart_repository.get_total_cart_price(cart_id=cart.id) == Decimal('0')


@pytest.mark.parametrize('expected_items_count', [1, 4, 6, 10, 20, 25, 29, 35, 43, 48, 50])
@pytest.mark.django_db
def test_get_cart_items_count_returns_correct_count(
    cart_repository: BaseCartRepository, cart: Cart, expected_items_count: int, seller: Seller
):
    CartItemModelFactory.create_batch(size=expected_items_count, cart=cart, seller=seller)
    assert cart_repository.get_cart_items_count(cart_id=cart.id) == expected_items_count


@pytest.mark.django_db
def test_get_cart_items_count_returns_zero_if_no_items(cart_repository: BaseCartRepository, cart: Cart):
    assert cart_repository.get_cart_items_count(cart_id=cart.id) == 0


@pytest.mark.django_db
def test_cart_item_exists_returns_true_if_item_exists(cart_repository: BaseCartRepository, cart_item: CartItem):
    assert (
        cart_repository.cart_item_exists(cart_id=cart_item.cart_id, product_variant_id=cart_item.product_variant_id)
        is True
    )


@pytest.mark.django_db
def test_cart_item_exists_returns_false_if_item_does_not_exist(
    cart_repository: BaseCartRepository, cart: Cart, product_variant: ProductVariant
):
    assert cart_repository.cart_item_exists(cart_id=cart.id, product_variant_id=product_variant.id) is False
