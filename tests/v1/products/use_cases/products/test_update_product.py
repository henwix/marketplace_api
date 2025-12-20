from uuid import uuid7

import pytest
from punq import Container

from src.apps.products.converters.products import product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import ProductAuthorPermissionError, ProductNotFoundByIdError
from src.apps.products.models.products import Product
from src.apps.products.use_cases.products.update import UpdateProductUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory
from tests.v1.products.test_data.new_product_data import PRODUCT_ARGNAMES, PRODUCT_ARGVALUES


@pytest.fixture
def update_product_use_case(container: Container) -> UpdateProductUseCase:
    return container.resolve(UpdateProductUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_ARGNAMES, argvalues=PRODUCT_ARGVALUES)
def test_product_updated_by_author(
    seller: Seller,
    update_product_use_case: UpdateProductUseCase,
    expected_title: str,
    expected_desc: str,
    expected_short_desc: str,
    expected_is_visible: bool,
):
    product = ProductModelFactory.create(seller=seller)
    db_product = Product.objects.get(pk=product.pk)
    assert product == db_product

    expected_data = {
        'title': expected_title,
        'description': expected_desc,
        'short_description': expected_short_desc,
        'is_visible': expected_is_visible,
    }
    updated_product = update_product_use_case.execute(
        seller=seller_to_entity(dto=seller), product_id=product.pk, data=expected_data
    )

    assert isinstance(updated_product, ProductEntity)
    db_product = Product.objects.get(pk=product.pk)
    assert updated_product == product_to_entity(dto=db_product)


@pytest.mark.django_db
def test_product_not_updated_if_seller_is_not_author(
    product: Product, seller: Seller, update_product_use_case: UpdateProductUseCase
):
    with pytest.raises(ProductAuthorPermissionError):
        update_product_use_case.execute(seller=seller_to_entity(dto=seller), product_id=product.pk, data={})
    db_product = Product.objects.get(pk=product.pk)
    assert db_product == product


@pytest.mark.django_db
def test_product_not_updated_if_not_exists(seller: Seller, update_product_use_case: UpdateProductUseCase):
    with pytest.raises(ProductNotFoundByIdError):
        update_product_use_case.execute(seller=seller_to_entity(dto=seller), product_id=uuid7(), data={})
