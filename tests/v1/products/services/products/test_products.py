from decimal import Decimal
from uuid import uuid7

import pytest
from django.db.models import Prefetch
from punq import Container

from src.apps.products.converters.products import product_from_entity, product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import ProductNotFoundByIdError, ProductNotFoundBySlugError
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.services.products import BaseProductService
from src.apps.sellers.converters.sellers import seller_to_entity
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
from tests.v1.products.test_data.product_data import PRODUCT_ARGNAMES, PRODUCT_ARGVALUES
from tests.v1.sellers.factories import SellerModelFactory


@pytest.fixture
def product_service(container: Container) -> BaseProductService:
    return container.resolve(BaseProductService)


@pytest.mark.django_db
def test_save_product_saved_for_creation(product_service: BaseProductService):
    product_entity = product_to_entity(ProductModelFactory.build(seller=SellerModelFactory.create()))
    assert not Product.objects.filter(pk=product_entity.id).exists()

    created_product = product_service.save(product=product_entity, update=False)
    db_product = Product.objects.get(pk=created_product.id)

    assert isinstance(created_product, ProductEntity)
    assert created_product == product_to_entity(dto=db_product)


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_ARGNAMES, argvalues=PRODUCT_ARGVALUES)
def test_save_product_saved_for_update(
    product_entity: ProductEntity,
    product_service: BaseProductService,
    expected_title: str,
    expected_desc: str,
    expected_short_desc: str,
    expected_is_visible: bool,
):
    product_entity.update(
        title=expected_title,
        description=expected_desc,
        short_description=expected_short_desc,
        is_visible=expected_is_visible,
    )

    saved_product = product_service.save(product=product_entity, update=True)
    assert isinstance(saved_product, ProductEntity)
    db_product = Product.objects.get(pk=product_entity.id)
    assert product_from_entity(saved_product) == db_product


@pytest.mark.django_db
def test_select_product_for_update_by_id_selected(product: Product, product_service: BaseProductService):
    retrieved_product = product_service.try_get_for_update_by_id(id=product.id)
    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(Product.objects.get(pk=product.id)) == retrieved_product


@pytest.mark.django_db
def test_select_product_for_update_by_id_not_selected_if_not_exists(product_service: BaseProductService):
    with pytest.raises(ProductNotFoundByIdError):
        product_service.try_get_for_update_by_id(id=uuid7())


@pytest.mark.django_db
def test_get_product_by_id_retrieved(product: Product, product_service: BaseProductService):
    retrieved_product = product_service.try_get_by_id(id=product.id)
    assert product_to_entity(Product.objects.get(pk=product.id)) == retrieved_product


@pytest.mark.django_db
def test_get_product_by_id_not_retrieved_if_not_exists_and_not_found_error_raised(product_service: BaseProductService):
    with pytest.raises(ProductNotFoundByIdError):
        product_service.try_get_by_id(id=uuid7())


@pytest.mark.django_db
def test_get_product_by_id_with_relations_retrieved(product: Product, product_service: BaseProductService):
    expected_variants = 9
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    retrieved_product = product_service.try_get_by_id_for_retrieve(id=product.pk)
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
def test_get_product_by_id_with_relations_and_and_not_visible_variants_retrieved(
    product: Product, product_service: BaseProductService
):
    expected_variants = 2
    expected_not_visible_variants = 6
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    retrieved_product = product_service.try_get_by_id_for_retrieve(id=product.pk)
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
def test_get_product_by_id_with_relations_not_retrieved_if_not_exists_and_not_found_error_raused(
    product_service: BaseProductService,
):
    with pytest.raises(ProductNotFoundByIdError):
        product_service.try_get_by_id_for_retrieve(id=uuid7())


@pytest.mark.django_db
def test_get_product_by_slug_with_relations_retrieved(product: Product, product_service: BaseProductService):
    expected_variants = 2
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    retrieved_product = product_service.try_get_by_slug_for_retrieve(slug=product.slug)
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
def test_get_product_by_slug_with_relations_and_not_visible_variants_retrieved(
    product: Product, product_service: BaseProductService
):
    expected_variants = 6
    expected_not_visible_variants = 4
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    retrieved_product = product_service.try_get_by_slug_for_retrieve(slug=product.slug)
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
def test_get_product_by_slug_with_relations_not_retrieved_if_not_exists_and_not_found_error_raised(
    product_service: BaseProductService,
):
    with pytest.raises(ProductNotFoundBySlugError):
        product_service.try_get_by_slug_for_retrieve(slug='test-slug')


@pytest.mark.django_db
def test_delete_product_deleted(product: Product, product_service: BaseProductService):
    assert Product.objects.filter(pk=product.pk).exists()
    product_service.delete(id=product.pk)
    assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_get_product_by_id_with_loaded_variants_retrieved(product_service: BaseProductService, product: Product):
    expected_visible_variants = 3
    expected_invisible_variants = 1
    expected_positive_stock_variants = 2
    expected_zero_stock_variants = 1
    expected_positive_price_variants = 1
    expected_negative_price_variants = 2
    expected_total_variants = (
        expected_visible_variants
        + expected_invisible_variants
        + expected_positive_stock_variants
        + expected_zero_stock_variants
        + expected_negative_price_variants
        + expected_positive_price_variants
    )

    ProductVariantModelFactory.create_batch(size=expected_visible_variants, is_visible=True, product=product)
    ProductVariantModelFactory.create_batch(size=expected_invisible_variants, is_visible=False, product=product)
    ProductVariantModelFactory.create_batch(size=expected_positive_stock_variants, stock=5, product=product)
    ProductVariantModelFactory.create_batch(size=expected_zero_stock_variants, stock=0, product=product)
    ProductVariantModelFactory.create_batch(
        size=expected_positive_price_variants,
        price=Decimal('123.40'),
        product=product,
    )
    ProductVariantModelFactory.create_batch(size=expected_negative_price_variants, price=Decimal('-1'), product=product)

    retrieved_product_entity = product_service.try_get_by_id_with_loaded_variants(id=product.pk)

    assert isinstance(retrieved_product_entity, ProductEntity)
    assert retrieved_product_entity.variants_count == expected_total_variants
    assert len(retrieved_product_entity.variants) == expected_total_variants


@pytest.mark.django_db
def test_get_product_by_id_with_loaded_variants_not_retrieved_if_not_exists(product_service: BaseProductService):
    with pytest.raises(ProductNotFoundByIdError):
        assert product_service.try_get_by_id_with_loaded_variants(id=uuid7())
