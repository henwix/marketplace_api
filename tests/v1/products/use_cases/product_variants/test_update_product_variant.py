from decimal import Decimal
from uuid import uuid7

import pytest
from punq import Container

from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.exceptions.product_variants import (
    ProductVariantAuthorPermissionError,
    ProductVariantNotFoundError,
)
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.use_cases.product_variants.update import UpdateProductVariantUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory


@pytest.fixture
def update_product_variant_use_case(container: Container) -> UpdateProductVariantUseCase:
    return container.resolve(UpdateProductVariantUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames=['expected_title', 'expected_price', 'expected_stock', 'expected_is_visible'],
    argvalues=[
        ('Test Variant Title', Decimal('34.99'), 13, True),
        ('VarriantTitleTest', Decimal('19399.99'), 105, False),
    ],
)
def test_update_variant_updated(
    update_product_variant_use_case: UpdateProductVariantUseCase,
    seller: Seller,
    expected_title: str,
    expected_price: Decimal,
    expected_stock: int,
    expected_is_visible: bool,
):
    expected_data = {
        'title': expected_title,
        'price': expected_price,
        'stock': expected_stock,
        'is_visible': expected_is_visible,
    }
    product = ProductModelFactory.create(seller=seller)
    product_variant = ProductVariantModelFactory.create(product=product)

    updated_product_variant = update_product_variant_use_case.execute(
        seller=seller_to_entity(dto=seller),
        product_variant_id=product_variant.pk,
        data=expected_data,
    )
    db_product_variant = ProductVariant.objects.get(pk=product_variant.id)
    assert ProductVariant.objects.filter(product_id=product.pk).count() == 1
    assert isinstance(updated_product_variant, ProductVariantEntity)
    assert product_variant_to_entity(dto=db_product_variant) == updated_product_variant


@pytest.mark.django_db
def test_update_variant_product_not_found_exception_raised(
    update_product_variant_use_case: UpdateProductVariantUseCase, seller: Seller
):
    with pytest.raises(ProductVariantNotFoundError):
        update_product_variant_use_case.execute(
            seller=seller_to_entity(dto=seller), product_variant_id=uuid7(), data={}
        )
    assert ProductVariant.objects.all().count() == 0


@pytest.mark.django_db
def test_update_variant_product_author_exception_raised(
    update_product_variant_use_case: UpdateProductVariantUseCase, seller: Seller, product_variant: ProductVariant
):
    with pytest.raises(ProductVariantAuthorPermissionError):
        update_product_variant_use_case.execute(
            seller=seller_to_entity(dto=seller), product_variant_id=product_variant.pk, data={}
        )
    assert ProductVariant.objects.all().count() == 1
