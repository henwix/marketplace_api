from uuid import uuid7

import pytest
from punq import Container

from src.apps.products.exceptions.product_variants import (
    ProductVariantAuthorPermissionError,
    ProductVariantNotFoundError,
)
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.use_cases.product_variants.delete import DeleteProductVariantUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory


@pytest.fixture
def delete_product_variant_use_case(container: Container) -> DeleteProductVariantUseCase:
    return container.resolve(DeleteProductVariantUseCase)


@pytest.mark.django_db
def test_delete_variant_deleted(
    delete_product_variant_use_case: DeleteProductVariantUseCase,
    seller: Seller,
):
    product = ProductModelFactory.create(seller=seller)
    product_variant = ProductVariantModelFactory.create(product=product)

    assert ProductVariant.objects.filter(product_id=product.pk).count() == 1
    delete_product_variant_use_case.execute(
        seller=seller_to_entity(dto=seller),
        product_variant_id=product_variant.pk,
    )
    assert ProductVariant.objects.filter(product_id=product.pk).count() == 0


@pytest.mark.django_db
def test_delete_variant_product_not_found_exception_raised(
    delete_product_variant_use_case: DeleteProductVariantUseCase, seller: Seller
):
    with pytest.raises(ProductVariantNotFoundError):
        delete_product_variant_use_case.execute(seller=seller_to_entity(dto=seller), product_variant_id=uuid7())
    assert ProductVariant.objects.all().count() == 0


@pytest.mark.django_db
def test_delete_variant_product_author_exception_raised(
    delete_product_variant_use_case: DeleteProductVariantUseCase, seller: Seller, product_variant: ProductVariant
):
    with pytest.raises(ProductVariantAuthorPermissionError):
        delete_product_variant_use_case.execute(
            seller=seller_to_entity(dto=seller), product_variant_id=product_variant.pk
        )
    assert ProductVariant.objects.all().count() == 1
