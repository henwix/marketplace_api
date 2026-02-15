import pytest

from src.apps.cart.converters import cart_item_to_entity, cart_to_entity
from src.apps.cart.entities import CartItemEntity
from src.apps.cart.exceptions import ItemAlreadyInCartError
from src.apps.cart.models import Cart, CartItem
from src.apps.cart.services.cart import BaseCartService
from src.apps.products.models.product_variants import ProductVariant
from src.apps.users.models import User


@pytest.mark.django_db
def test_get_cart_retrieved(cart_service: BaseCartService, user: User):
    db_cart = Cart.objects.create(user=user)
    retrieved_cart = cart_service.get_or_create_cart(user_id=user.id)
    assert retrieved_cart == cart_to_entity(dto=db_cart)


@pytest.mark.django_db
def test_create_cart_created(cart_service: BaseCartService, user: User):
    created_cart = cart_service.get_or_create_cart(user_id=user.id)
    db_cart = Cart.objects.get(user=user)
    assert created_cart == cart_to_entity(dto=db_cart)


@pytest.mark.django_db
def test_save_cart_item_saved(cart_service: BaseCartService, user: User, product_variant: ProductVariant):
    cart = Cart.objects.create(user=user)
    cart_item_entity = CartItemEntity.create(
        cart_id=cart.id,
        product_variant_id=product_variant.id,
        seller_id=product_variant.product.seller.id,
        quantity=3,
        price_snapshot=product_variant.price,
    )
    new_cart_item = cart_service.save_cart_item(cart_item=cart_item_entity, update=False)
    db_cart_item = CartItem.objects.get(cart=cart, product_variant=product_variant)
    assert new_cart_item == cart_item_to_entity(dto=db_cart_item)


@pytest.mark.django_db
def test_create_cart_not_created_and_item_already_in_cart_error_raised(
    cart_service: BaseCartService,
    user: User,
    product_variant: ProductVariant,
):
    cart = Cart.objects.create(user=user)
    cart_item_entity = CartItemEntity.create(
        cart_id=cart.id,
        product_variant_id=product_variant.id,
        seller_id=product_variant.product.seller.id,
        quantity=3,
        price_snapshot=product_variant.price,
    )
    cart_service.save_cart_item(cart_item=cart_item_entity, update=False)

    with pytest.raises(ItemAlreadyInCartError):
        cart_service.save_cart_item(cart_item=cart_item_entity, update=False)
