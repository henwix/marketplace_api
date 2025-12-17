import pytest
from punq import Container

from src.apps.products.converters.products import product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.models.products import Product
from src.apps.products.use_cases.products.create import CreateProductUseCase
from src.apps.sellers.models import Seller
from tests.v1.products.test_data.new_product_data import PRODUCT_ARGNAMES, PRODUCT_ARGVALUES


@pytest.fixture
def create_product_use_case(container: Container) -> CreateProductUseCase:
    return container.resolve(CreateProductUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_ARGNAMES, argvalues=PRODUCT_ARGVALUES)
def test_product_created(
    seller: Seller,
    create_product_use_case: CreateProductUseCase,
    expected_title: str,
    expected_desc: str,
    expected_short_desc: str,
    expected_is_visible: bool,
):
    expected_data = {
        'title': expected_title,
        'description': expected_desc,
        'short_description': expected_short_desc,
        'is_visible': expected_is_visible,
    }

    created_product = create_product_use_case.execute(seller_id=seller.pk, data=expected_data)
    db_product = Product.objects.get(pk=created_product.id)

    assert isinstance(created_product, ProductEntity)
    assert product_to_entity(dto=db_product) == created_product
