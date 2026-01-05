from decimal import Decimal

import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.products.commands.products import PersonalSearchProductCommand
from src.apps.products.use_cases.products.personal_search import PersonalSearchProductUseCase
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.products.utils import create_test_products_with_variant
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def personal_search_product_use_case(container: Container) -> PersonalSearchProductUseCase:
    return container.resolve(PersonalSearchProductUseCase)


@pytest.mark.django_db
def test_personal_search_products_retrieved(
    personal_search_product_use_case: PersonalSearchProductUseCase,
    seller: Seller,
):
    expected_personal_product_count = 11
    create_test_products_with_variant(
        products_params={'size': expected_personal_product_count, 'is_visible': False, 'seller': seller},
        variant_params={'price': Decimal('11.99')},
    )
    create_test_products_with_variant(
        products_params={'size': 4, 'is_visible': True},
        variant_params={'price': Decimal('9.99')},
    )

    command = PersonalSearchProductCommand(user_id=seller.user_id)
    retrieved_products = personal_search_product_use_case.execute(command=command)
    assert len(retrieved_products) == expected_personal_product_count


@pytest.mark.django_db
def test_personal_search_seller_not_found_error_raised(
    personal_search_product_use_case: PersonalSearchProductUseCase,
    user: User,
):
    command = PersonalSearchProductCommand(user_id=user.pk)
    with pytest.raises(SellerNotFoundError):
        personal_search_product_use_case.execute(command=command)


@pytest.mark.django_db
def test_personal_search_user_credentials_error_raised(personal_search_product_use_case: PersonalSearchProductUseCase):
    command = PersonalSearchProductCommand(user_id=None)
    with pytest.raises(AuthCredentialsNotProvidedError):
        personal_search_product_use_case.execute(command=command)


@pytest.mark.django_db
def test_personal_search_user_not_found_error_raised(personal_search_product_use_case: PersonalSearchProductUseCase):
    command = PersonalSearchProductCommand(user_id=1)
    with pytest.raises(UserNotFoundError):
        personal_search_product_use_case.execute(command=command)


@pytest.mark.django_db
def test_personal_search_user_not_active_error_raised(personal_search_product_use_case: PersonalSearchProductUseCase):
    user = UserModelFactory.create(is_active=False)
    command = PersonalSearchProductCommand(user_id=user.pk)
    with pytest.raises(UserNotActiveError):
        personal_search_product_use_case.execute(command=command)
