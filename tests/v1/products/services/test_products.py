from uuid import uuid7

import pytest
from django.db.models import Prefetch

from src.apps.products.converters.products import product_from_entity, product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import ProductNotFoundError
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.services.products import BaseProductService
from src.apps.sellers.converters.sellers import seller_to_entity
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
from tests.v1.products.test_data.new_product_data import PRODUCT_ARGNAMES, PRODUCT_ARGVALUES
from tests.v1.sellers.factories import SellerModelFactory


@pytest.mark.django_db
def test_product_saved_for_creation(product_service: BaseProductService):
    product_entity = product_to_entity(ProductModelFactory.build(seller=SellerModelFactory.create()))
    assert not Product.objects.filter(pk=product_entity.id).exists()

    saved_product = product_service.save(product=product_entity, update=False)
    db_product = Product.objects.get(pk=saved_product.id)

    assert isinstance(saved_product, ProductEntity)
    assert saved_product == product_to_entity(dto=db_product)
    assert Product.objects.filter(pk=product_entity.id).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_ARGNAMES, argvalues=PRODUCT_ARGVALUES)
def test_product_saved_for_update(
    product_entity: ProductEntity,
    product_service: BaseProductService,
    expected_title: str,
    expected_desc: str,
    expected_short_desc: str,
    expected_is_visible: bool,
):
    product_entity.update_from_data(
        data={
            'title': expected_title,
            'description': expected_desc,
            'short_description': expected_short_desc,
            'is_visible': expected_is_visible,
        }
    )

    saved_product = product_service.save(product=product_entity, update=True)
    assert isinstance(saved_product, ProductEntity)
    db_product = Product.objects.get(pk=product_entity.id)
    assert product_from_entity(saved_product) == db_product


@pytest.mark.django_db
def test_product_selected_for_update_by_id(product: Product, product_service: BaseProductService):
    retrieved_product = product_service.select_for_update_by_id_or_404(id=product.id)
    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(Product.objects.get(pk=product.id)) == retrieved_product


@pytest.mark.django_db
def test_product_not_selected_for_update_by_id_and_raised_if_not_exists(product_service: BaseProductService):
    with pytest.raises(ProductNotFoundError):
        product_service.select_for_update_by_id_or_404(id=uuid7())


@pytest.mark.django_db
def test_product_retrieved_by_id(product: Product, product_service: BaseProductService):
    retrieved_product = product_service.get_by_id_or_404(id=product.id)
    assert product_to_entity(Product.objects.get(pk=product.id)) == retrieved_product


@pytest.mark.django_db
def test_product_not_retrieved_by_id_if_not_exists(product_service: BaseProductService):
    with pytest.raises(ProductNotFoundError):
        product_service.get_by_id_or_404(id=uuid7())


@pytest.mark.django_db
def test_product_retrieved_by_id_with_relations(product: Product, product_service: BaseProductService):
    expected_variants = 9
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    retrieved_product = product_service.get_by_id_for_retrieve_or_404(id=product.pk)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product
    assert retrieved_product.seller == seller_to_entity(product.seller)
    assert len(retrieved_product.variants) == expected_variants


@pytest.mark.django_db
def test_product_retrieved_by_id_with_relations_and_zero_price(product: Product, product_service: BaseProductService):
    expected_variants = 4
    expected_variants_with_zero_price = 2
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_variants_with_zero_price, product=product, price=0)
    retrieved_product = product_service.get_by_id_for_retrieve_or_404(id=product.pk)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product
    assert len(retrieved_product.variants) == expected_variants


@pytest.mark.django_db
def test_product_retrieved_by_id_with_relations_and_not_visible_variants(
    product: Product, product_service: BaseProductService
):
    expected_variants = 2
    expected_not_visible_variants = 6
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    retrieved_product = product_service.get_by_id_for_retrieve_or_404(id=product.pk)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product
    assert len(retrieved_product.variants) == expected_variants


@pytest.mark.django_db
def test_product_not_retrieved_by_id_with_relations_if_not_exists(product_service: BaseProductService):
    with pytest.raises(ProductNotFoundError):
        product_service.get_by_id_for_retrieve_or_404(id=uuid7())


@pytest.mark.django_db
def test_product_retrieved_by_slug_with_relations(product: Product, product_service: BaseProductService):
    expected_variants = 2
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    retrieved_product = product_service.get_by_slug_for_retrieve_or_404(slug=product.slug)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product
    assert retrieved_product.seller == seller_to_entity(product.seller)
    assert len(retrieved_product.variants) == expected_variants


@pytest.mark.django_db
def test_product_retrieved_by_slug_with_relations_and_zero_price(product: Product, product_service: BaseProductService):
    expected_variants = 1
    expected_variants_with_zero_price = 7
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_variants_with_zero_price, product=product, price=0)
    retrieved_product = product_service.get_by_slug_for_retrieve_or_404(slug=product.slug)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product
    assert len(retrieved_product.variants) == expected_variants


@pytest.mark.django_db
def test_product_retrieved_by_slug_with_relations_and_not_visible_variants(
    product: Product, product_service: BaseProductService
):
    expected_variants = 6
    expected_not_visible_variants = 4
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    retrieved_product = product_service.get_by_slug_for_retrieve_or_404(slug=product.slug)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product
    assert len(retrieved_product.variants) == expected_variants


@pytest.mark.django_db
def test_product_not_retrieved_by_slug_with_relations_if_not_exists(product_service: BaseProductService):
    with pytest.raises(ProductNotFoundError):
        product_service.get_by_slug_for_retrieve_or_404(slug='test-slug')


@pytest.mark.django_db
def test_product_deleted(product: Product, product_service: BaseProductService):
    assert Product.objects.filter(pk=product.pk).exists()
    product_service.delete(id=product.pk)
    assert not Product.objects.filter(pk=product.pk).exists()
