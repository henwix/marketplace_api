from decimal import Decimal

import pytest
from punq import Container

from src.apps.products.use_cases.products.global_search import GlobalSearchProductUseCase
from tests.v1.products.utils import create_test_products_with_variant


@pytest.fixture
def global_search_product_use_case(container: Container) -> GlobalSearchProductUseCase:
    return container.resolve(GlobalSearchProductUseCase)


@pytest.mark.django_db
def test_global_search_products_retrieved(global_search_product_use_case: GlobalSearchProductUseCase):
    expected_products_count = 8
    create_test_products_with_variant(
        products_params={'size': expected_products_count, 'is_visible': True},
        variant_params={'price': Decimal('99.99')},
    )

    retrieved_products = global_search_product_use_case.execute()
    assert len(retrieved_products) == expected_products_count
