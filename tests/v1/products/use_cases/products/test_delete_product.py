from uuid import uuid7

import pytest
from punq import Container

from src.apps.products.exceptions.products import ProductAuthorPermissionError, ProductNotFoundByIdError
from src.apps.products.models.products import Product
from src.apps.products.use_cases.products.delete import DeleteProductUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory


@pytest.fixture
def delete_product_use_case(container: Container) -> DeleteProductUseCase:
    return container.resolve(DeleteProductUseCase)


@pytest.mark.django_db
def test_product_deleted(seller: Seller, delete_product_use_case: DeleteProductUseCase):
    product = ProductModelFactory.create(seller=seller)
    assert Product.objects.filter(pk=product.pk).exists()
    delete_product_use_case.execute(seller=seller_to_entity(dto=seller), product_id=product.pk)
    assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_product_not_deleted_if_seller_is_not_author(
    seller: Seller, product: Product, delete_product_use_case: DeleteProductUseCase
):
    with pytest.raises(ProductAuthorPermissionError):
        delete_product_use_case.execute(seller=seller_to_entity(dto=seller), product_id=product.pk)
    assert Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_product_not_deleted_if_not_exists(seller: Seller, delete_product_use_case: DeleteProductUseCase):
    with pytest.raises(ProductNotFoundByIdError):
        delete_product_use_case.execute(seller=seller_to_entity(dto=seller), product_id=uuid7())
