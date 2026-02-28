from uuid import uuid7

import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.cart.commands import AddItemToCartCommand
from src.apps.cart.converters import cart_item_to_entity
from src.apps.cart.exceptions import CartLimitError, ItemAlreadyInCartError
from src.apps.cart.models import Cart, CartItem
from src.apps.cart.use_cases.add_item_to_cart import AddItemToCartUseCase
from src.apps.products.exceptions.product_variants import (
    ProductVariantAccessForbiddenError,
    ProductVariantNotFoundError,
    ProductVariantOutOfStockError,
    QuantityGreaterThanStockError,
)
from src.apps.products.models.product_variants import ProductVariant
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.cart.factories import CartItemModelFactory
from tests.v1.products.factories import ProductVariantModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def add_item_to_cart_use_case(container: Container) -> AddItemToCartUseCase:
    return container.resolve(AddItemToCartUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize('expected_quantity', [1, 7, 13, 22, 33, 125, 542, 1002, 3521])
def test_add_item_with_existing_cart(
    add_item_to_cart_use_case: AddItemToCartUseCase,
    user: User,
    expected_quantity: int,
):
    cart = Cart.objects.create(user=user)
    product_variant = ProductVariantModelFactory.create(stock=5000)
    command = AddItemToCartCommand(
        user_id=user.id,
        product_variant_id=product_variant.id,
        quantity=expected_quantity,
    )
    created_cart_item = add_item_to_cart_use_case.execute(command=command)
    db_cart_item = CartItem.objects.get(cart=cart, product_variant=product_variant)

    assert created_cart_item == cart_item_to_entity(dto=db_cart_item)
    assert created_cart_item.cart_id == cart.id
    assert created_cart_item.price_snapshot == product_variant.price
    assert created_cart_item.product_variant_id == product_variant.id
    assert created_cart_item.quantity == expected_quantity
    assert created_cart_item.seller_id == product_variant.product.seller.id


@pytest.mark.django_db
@pytest.mark.parametrize('expected_quantity', [1, 7, 13, 22, 33, 125, 542, 1002, 3521])
def test_add_item_with_no_existing_cart(
    add_item_to_cart_use_case: AddItemToCartUseCase,
    user: User,
    expected_quantity: int,
):
    product_variant = ProductVariantModelFactory.create(stock=5000)
    command = AddItemToCartCommand(
        user_id=user.id,
        product_variant_id=product_variant.id,
        quantity=expected_quantity,
    )
    created_cart_item = add_item_to_cart_use_case.execute(command=command)
    user_cart = Cart.objects.get(user=user)
    db_cart_item = CartItem.objects.get(cart=user_cart, product_variant=product_variant)

    assert product_variant in user_cart.product_variants.all()
    assert created_cart_item == cart_item_to_entity(dto=db_cart_item)
    assert created_cart_item.cart_id == user_cart.id
    assert created_cart_item.price_snapshot == product_variant.price
    assert created_cart_item.product_variant_id == product_variant.id
    assert created_cart_item.quantity == expected_quantity
    assert created_cart_item.seller_id == product_variant.product.seller.id


@pytest.mark.django_db
def test_add_item_not_added_and_product_variant_not_found_error_raised(
    add_item_to_cart_use_case: AddItemToCartUseCase,
    user: User,
):
    command = AddItemToCartCommand(
        user_id=user.id,
        product_variant_id=uuid7(),
        quantity=1,
    )
    with pytest.raises(ProductVariantNotFoundError):
        add_item_to_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_add_item_not_added_and_product_already_in_cart_error_raised(
    add_item_to_cart_use_case: AddItemToCartUseCase,
    user: User,
):
    product_variant = ProductVariantModelFactory.create(stock=5000)
    command = AddItemToCartCommand(
        user_id=user.id,
        product_variant_id=product_variant.id,
        quantity=1,
    )
    add_item_to_cart_use_case.execute(command=command)

    with pytest.raises(ItemAlreadyInCartError):
        add_item_to_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_add_item_not_added_and_product_access_forbidden_error_raised_if_variant_is_not_visible(
    add_item_to_cart_use_case: AddItemToCartUseCase,
    user: User,
):
    product_variant = ProductVariantModelFactory.create(stock=5000, is_visible=False)
    command = AddItemToCartCommand(
        user_id=user.id,
        product_variant_id=product_variant.id,
        quantity=1,
    )
    with pytest.raises(ProductVariantAccessForbiddenError):
        add_item_to_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_add_item_not_added_and_product_variant_out_of_stock_error_raised(
    add_item_to_cart_use_case: AddItemToCartUseCase,
    user: User,
):
    product_variant = ProductVariantModelFactory.create(stock=0)
    command = AddItemToCartCommand(
        user_id=user.id,
        product_variant_id=product_variant.id,
        quantity=1,
    )
    with pytest.raises(ProductVariantOutOfStockError):
        add_item_to_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_add_item_not_added_and_quantity_greater_than_stock_error_raised(
    add_item_to_cart_use_case: AddItemToCartUseCase,
    user: User,
):
    expected_stock = 5
    expected_quantity = 10
    product_variant = ProductVariantModelFactory.create(stock=expected_stock)
    command = AddItemToCartCommand(
        user_id=user.id,
        product_variant_id=product_variant.id,
        quantity=expected_quantity,
    )
    with pytest.raises(QuantityGreaterThanStockError):
        add_item_to_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_add_item_not_added_and_cart_limit_error_raised(
    add_item_to_cart_use_case: AddItemToCartUseCase,
    cart: Cart,
    product_variant: ProductVariant,
):
    CartItemModelFactory.create_batch(size=50, cart=cart)
    with pytest.raises(CartLimitError):
        command = AddItemToCartCommand(user_id=cart.user_id, product_variant_id=product_variant.id, quantity=1)
        add_item_to_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_add_item_credentials_error_raised(add_item_to_cart_use_case: AddItemToCartUseCase):
    command = AddItemToCartCommand(user_id=None, product_variant_id=uuid7(), quantity=1)
    with pytest.raises(AuthCredentialsNotProvidedError):
        add_item_to_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_add_item_user_not_found_error_raised(add_item_to_cart_use_case: AddItemToCartUseCase):
    command = AddItemToCartCommand(user_id=1, product_variant_id=uuid7(), quantity=1)
    with pytest.raises(UserNotFoundError):
        add_item_to_cart_use_case.execute(command=command)


@pytest.mark.django_db
def test_add_item_user_not_active_error_raised(add_item_to_cart_use_case: AddItemToCartUseCase):
    user = UserModelFactory.create(is_active=False)
    command = AddItemToCartCommand(user_id=user.pk, product_variant_id=uuid7(), quantity=1)
    with pytest.raises(UserNotActiveError):
        add_item_to_cart_use_case.execute(command=command)
