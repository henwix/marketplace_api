from decimal import Decimal
from uuid import uuid7

import pytest

from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.exceptions.product_variants import ProductVariantNotFoundError
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.services.product_variants import BaseProductVariantService
from tests.v1.products.factories import ProductVariantModelFactory


@pytest.mark.django_db
def test_save_variant_saved_for_creation(
    variant_service: BaseProductVariantService,
    product: Product,
):
    product_variant_entity = product_variant_to_entity(dto=ProductVariantModelFactory.build(product=product))
    assert not ProductVariant.objects.filter(pk=product_variant_entity.id).exists()

    created_product_variant = variant_service.save(product_variant=product_variant_entity, update=False)
    db_product_variant = ProductVariant.objects.get(pk=product_variant_entity.id)

    assert isinstance(created_product_variant, ProductVariantEntity)
    assert created_product_variant.id == db_product_variant.pk
    assert created_product_variant.title == db_product_variant.title
    assert created_product_variant.price == db_product_variant.price
    assert created_product_variant.stock == db_product_variant.stock
    assert created_product_variant.product_id == db_product_variant.product_id
    assert created_product_variant.is_visible == db_product_variant.is_visible
    assert created_product_variant.created_at == db_product_variant.created_at
    assert created_product_variant.updated_at == db_product_variant.updated_at


@pytest.mark.django_db
def test_save_variant_saved_for_update(
    variant_service: BaseProductVariantService,
    product_variant: ProductVariant,
):
    product_variant.title = 'test variant title'
    product_variant.price = Decimal('7424.89')
    product_variant.stock = 572
    product_variant.is_visible = False

    updated_product_variant = variant_service.save(
        product_variant=product_variant_to_entity(dto=product_variant), update=True
    )
    db_product_variant = ProductVariant.objects.get(pk=product_variant.pk)

    assert isinstance(updated_product_variant, ProductVariantEntity)
    assert updated_product_variant.id == db_product_variant.id
    assert updated_product_variant.title == db_product_variant.title
    assert updated_product_variant.price == db_product_variant.price
    assert updated_product_variant.stock == db_product_variant.stock
    assert updated_product_variant.product_id == db_product_variant.product_id
    assert updated_product_variant.is_visible == db_product_variant.is_visible
    assert updated_product_variant.created_at == db_product_variant.created_at
    assert updated_product_variant.updated_at == db_product_variant.updated_at


@pytest.mark.django_db
def test_get_by_id_with_loaded_product_retrieved(
    variant_service: BaseProductVariantService,
    product_variant: ProductVariant,
):
    retrieved_variant = variant_service.try_get_by_id_with_loaded_product(id=product_variant.pk)
    assert isinstance(retrieved_variant, ProductVariantEntity)
    assert product_variant.pk == retrieved_variant.id
    assert product_variant.title == retrieved_variant.title
    assert product_variant.price == retrieved_variant.price
    assert product_variant.stock == retrieved_variant.stock
    assert product_variant.is_visible == retrieved_variant.is_visible
    assert product_variant.product.seller_id == retrieved_variant.product_seller_id


@pytest.mark.django_db
def test_get_by_id_with_loaded_product_not_retrieved_if_not_exists(variant_service: BaseProductVariantService):
    with pytest.raises(ProductVariantNotFoundError):
        variant_service.try_get_by_id_with_loaded_product(id=uuid7())


@pytest.mark.django_db
def test_delete_variant_deleted(variant_service: BaseProductVariantService, product_variant: ProductVariant):
    assert ProductVariant.objects.filter(pk=product_variant.pk).exists()
    variant_service.delete(id=product_variant.pk)
    assert not ProductVariant.objects.filter(pk=product_variant.pk).exists()
