import factory
from factory.django import DjangoModelFactory

from src.apps.users.models import User


class UserModelFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = factory.Faker('phone_number')
    password = factory.Faker('password')
