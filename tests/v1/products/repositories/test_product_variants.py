from decimal import Decimal
from uuid import uuid7

import pytest
from punq import Container

from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.repositories.product_variants import BaseProductVariantRepository
from tests.v1.products.factories import ProductVariantModelFactory


@pytest.fixture
def variant_repository(container: Container) -> BaseProductVariantRepository:
    return container.resolve(BaseProductVariantRepository)


@pytest.mark.django_db
def test_save_variant_saved_for_creation(variant_repository: BaseProductVariantRepository, product: Product):
    product_variant = ProductVariantModelFactory.build(product=product)
    assert not ProductVariant.objects.filter(pk=product_variant.pk).exists()

    created_product_variant = variant_repository.save(
        product_variant=product_variant_to_entity(dto=product_variant), update=False
    )
    db_product_variant = ProductVariant.objects.get(pk=product_variant.pk)

    assert isinstance(created_product_variant, ProductVariantEntity)
    assert created_product_variant == product_variant_to_entity(dto=db_product_variant)
    assert created_product_variant.id == db_product_variant.pk
    assert created_product_variant.title == db_product_variant.title
    assert created_product_variant.price == db_product_variant.price
    assert created_product_variant.stock == db_product_variant.stock
    assert created_product_variant.product_id == db_product_variant.product.id
    assert created_product_variant.is_visible == db_product_variant.is_visible
    assert created_product_variant.created_at == db_product_variant.created_at
    assert created_product_variant.updated_at == db_product_variant.updated_at
    assert product_variant.title == db_product_variant.title
    assert product_variant.price == db_product_variant.price
    assert product_variant.stock == db_product_variant.stock
    assert product_variant.is_visible == db_product_variant.is_visible
    assert product_variant.product == db_product_variant.product


@pytest.mark.django_db
def test_save_variant_saved_for_update(
    variant_repository: BaseProductVariantRepository,
    product_variant: ProductVariant,
):
    product_variant.title = 'test variant title'
    product_variant.price = Decimal('7424.89')
    product_variant.stock = 572
    product_variant.is_visible = False

    updated_product_variant = variant_repository.save(
        product_variant=product_variant_to_entity(dto=product_variant), update=True
    )
    db_product_variant = ProductVariant.objects.get(pk=product_variant.pk)

    assert isinstance(updated_product_variant, ProductVariantEntity)
    assert updated_product_variant == product_variant_to_entity(dto=db_product_variant)
    assert updated_product_variant.id == db_product_variant.pk
    assert updated_product_variant.title == db_product_variant.title
    assert updated_product_variant.price == db_product_variant.price
    assert updated_product_variant.stock == db_product_variant.stock
    assert updated_product_variant.product_id == db_product_variant.product.id
    assert updated_product_variant.is_visible == db_product_variant.is_visible
    assert updated_product_variant.created_at == db_product_variant.created_at
    assert updated_product_variant.updated_at == db_product_variant.updated_at
    assert product_variant.title == db_product_variant.title
    assert product_variant.price == db_product_variant.price
    assert product_variant.stock == db_product_variant.stock
    assert product_variant.is_visible == db_product_variant.is_visible
    assert product_variant.product == db_product_variant.product


@pytest.mark.django_db
@pytest.mark.parametrize('expected_variants_count', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_get_variants_count_retrieved(
    variant_repository: BaseProductVariantRepository,
    product: Product,
    expected_variants_count: int,
):
    ProductVariantModelFactory.create_batch(size=expected_variants_count, product=product)
    assert variant_repository.get_variants_count(product_id=product.pk) == expected_variants_count


@pytest.mark.django_db
def test_get_variants_count_retrieved_zero_if_no_variants_exists(
    variant_repository: BaseProductVariantRepository,
    product: Product,
):
    assert variant_repository.get_variants_count(product_id=product.pk) == 0


@pytest.mark.django_db
def test_get_by_id_with_loaded_product_retrieved(
    variant_repository: BaseProductVariantRepository,
    product_variant: ProductVariant,
):
    retrieved_variant = variant_repository.get_by_id_with_loaded_product(id=product_variant.pk)
    assert isinstance(retrieved_variant, ProductVariantEntity)
    assert product_variant.pk == retrieved_variant.id
    assert product_variant.title == retrieved_variant.title
    assert product_variant.price == retrieved_variant.price
    assert product_variant.stock == retrieved_variant.stock
    assert product_variant.is_visible == retrieved_variant.is_visible
    assert product_variant.product.seller_id == retrieved_variant.product_seller_id


@pytest.mark.django_db
def test_get_by_id_with_loaded_product_not_retrieved_if_not_exists(variant_repository: BaseProductVariantRepository):
    retrieved_variant = variant_repository.get_by_id_with_loaded_product(id=uuid7())
    assert retrieved_variant is None


@pytest.mark.django_db
def test_delete_variant_deleted(variant_repository: BaseProductVariantRepository, product_variant: ProductVariant):
    assert ProductVariant.objects.filter(pk=product_variant.pk).exists()
    variant_repository.delete(id=product_variant.pk)
    assert not ProductVariant.objects.filter(pk=product_variant.pk).exists()
