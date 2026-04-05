import factory
from factory.django import DjangoModelFactory
from faker import Faker

from src.apps.authentication.models.auth_provider import AuthProvider
from tests.v1.factories import lazy_function_factory
from tests.v1.users.factories import UserModelFactory

fake = Faker()


class AuthProviderModelFactory(DjangoModelFactory):
    class Meta:
        model = AuthProvider

    user = factory.SubFactory(factory=UserModelFactory)
    provider = lazy_function_factory(value=fake.uuid4, max_length=32)
    provider_uid = lazy_function_factory(value=fake.uuid4, max_length=32)
