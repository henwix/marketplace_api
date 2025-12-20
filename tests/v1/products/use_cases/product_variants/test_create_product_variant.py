from decimal import Decimal
from uuid import uuid7

import pytest
from punq import Container

from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.exceptions.product_variants import ProductVariantsLimitError
from src.apps.products.exceptions.products import ProductAuthorPermissionError, ProductNotFoundByIdError
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.use_cases.product_variants.create import CreateProductVariantUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory


@pytest.fixture
def create_product_variant_use_case(container: Container) -> CreateProductVariantUseCase:
    return container.resolve(CreateProductVariantUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames=['expected_title', 'expected_price', 'expected_stock', 'expected_is_visible'],
    argvalues=[
        ('Test Variant Title', Decimal('34.99'), 13, True),
        ('VarriantTitleTest', Decimal('19399.99'), 105, False),
    ],
)
def test_create_variant_created(
    create_product_variant_use_case: CreateProductVariantUseCase,
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
    assert ProductVariant.objects.filter(product_id=product.pk).count() == 0

    created_product_variant = create_product_variant_use_case.execute(
        seller=seller_to_entity(dto=seller), data=expected_data, product_id=product.pk
    )
    db_product_variant = ProductVariant.objects.get(pk=created_product_variant.id)
    assert ProductVariant.objects.filter(product_id=product.pk).count() == 1
    assert isinstance(created_product_variant, ProductVariantEntity)
    assert product_variant_to_entity(dto=db_product_variant) == created_product_variant


@pytest.mark.django_db
def test_create_variant_product_not_found_exception_raised(
    create_product_variant_use_case: CreateProductVariantUseCase, seller: Seller
):
    with pytest.raises(ProductNotFoundByIdError):
        create_product_variant_use_case.execute(seller=seller_to_entity(dto=seller), data={}, product_id=uuid7())
    assert ProductVariant.objects.all().count() == 0


@pytest.mark.django_db
def test_create_variant_author_exception_raised(
    create_product_variant_use_case: CreateProductVariantUseCase, seller: Seller, product: Product
):
    with pytest.raises(ProductAuthorPermissionError):
        create_product_variant_use_case.execute(seller=seller_to_entity(dto=seller), data={}, product_id=product.pk)
    assert ProductVariant.objects.all().count() == 0


@pytest.mark.django_db
def test_create_variant_limit_exception_raised(
    create_product_variant_use_case: CreateProductVariantUseCase, seller: Seller
):
    product = ProductModelFactory.create(seller=seller)
    ProductVariantModelFactory.create_batch(size=10, product=product)
    assert ProductVariant.objects.all().count() == 10
    with pytest.raises(ProductVariantsLimitError):
        create_product_variant_use_case.execute(seller=seller_to_entity(dto=seller), data={}, product_id=product.pk)
    assert ProductVariant.objects.all().count() == 10
