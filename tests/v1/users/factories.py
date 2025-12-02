import factory
from factory.django import DjangoModelFactory
from faker import Faker

from src.apps.users.models import User
from tests.v1.factories import lazy_function_factory

fake = Faker()


class UserModelFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = lazy_function_factory(value=fake.phone_number, max_length=20)
    password = factory.Faker('password')
