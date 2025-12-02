import factory
from factory.django import DjangoModelFactory
from faker import Faker

from src.apps.sellers.models import Seller
from tests.v1.factories import lazy_function_factory
from tests.v1.users.factories import UserModelFactory

fake = Faker()


class SellerModelFactory(DjangoModelFactory):
    class Meta:
        model = Seller

    user = factory.SubFactory(UserModelFactory)
    name = lazy_function_factory(value=fake.name, max_length=100)
    description = factory.Faker('text')
