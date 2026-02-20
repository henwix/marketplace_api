import pytest
from django.db.models import Count

from src.apps.products.converters.products import product_from_entity, product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.models.products import Product
from tests.v1.products.factories import ProductVariantModelFactory


@pytest.mark.django_db
def test_convert_product_to_entity(product: Product):
    ProductVariantModelFactory.create_batch(size=8, product=product)
    db_product = (
        Product.objects.annotate(variants_count=Count('variants'))
        .select_related('seller')
        .prefetch_related('variants')
        .filter(pk=product.pk)
        .first()
    )
    converted_entity = product_to_entity(dto=db_product)

    assert isinstance(converted_entity, ProductEntity)
    assert converted_entity.id == db_product.pk
    assert converted_entity.slug == db_product.slug
    assert converted_entity.seller_id == db_product.seller_id
    assert converted_entity.seller is None
    assert converted_entity.variants is None
    assert converted_entity.variants_count == db_product.variants_count
    assert converted_entity.title == db_product.title
    assert converted_entity.description == db_product.description
    assert converted_entity.short_description == db_product.short_description
    assert converted_entity.is_visible == db_product.is_visible
    assert converted_entity.created_at == db_product.created_at
    assert converted_entity.updated_at == db_product.updated_at


@pytest.mark.django_db
def test_convert_product_from_entity(product: Product):
    converted_entity = product_to_entity(dto=product)
    converted_product = product_from_entity(entity=converted_entity)

    assert isinstance(converted_product, Product)
    assert converted_entity.id == product.pk
    assert converted_entity.slug == product.slug
    assert converted_entity.seller_id == product.seller_id
    assert converted_entity.title == product.title
    assert converted_entity.description == product.description
    assert converted_entity.short_description == product.short_description
    assert converted_entity.is_visible == product.is_visible
    assert converted_entity.created_at == product.created_at
    assert converted_entity.updated_at == product.updated_at
