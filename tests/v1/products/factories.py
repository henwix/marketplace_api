import factory
from factory.django import DjangoModelFactory
from faker import Faker

from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from tests.v1.factories import lazy_function_factory
from tests.v1.sellers.factories import SellerModelFactory

fake = Faker()


class ProductModelFactory(DjangoModelFactory):
    class Meta:
        model = Product

    slug = lazy_function_factory(value=fake.slug, max_length=300)
    seller = factory.SubFactory(SellerModelFactory)
    title = lazy_function_factory(value=fake.text, max_length=255)
    description = factory.Faker('text')
    short_description = lazy_function_factory(value=fake.text, max_length=500)


class ProductVariantModelFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductModelFactory)
    title = lazy_function_factory(value=fake.text, max_length=200)
    price = fake.pydecimal(left_digits=2, right_digits=10, positive=True)
    stock = factory.Faker('random_int')
