import factory
from factory.django import DjangoModelFactory
from faker import Faker

from src.apps.cart.models import Cart, CartItem
from tests.v1.products.factories import ProductVariantModelFactory
from tests.v1.sellers.factories import SellerModelFactory
from tests.v1.users.factories import UserModelFactory

fake = Faker()


class CartModelFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserModelFactory)


class CartItemModelFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartModelFactory)
    product_variant = factory.SubFactory(ProductVariantModelFactory)
    seller = factory.SubFactory(SellerModelFactory)
    quantity = fake.pyint(min_value=1, max_value=2147483647)
    price_snapshot = fake.pydecimal(left_digits=2, right_digits=2, positive=True)
