from uuid import uuid7

import pytest
from django.db.models import Prefetch
from punq import Container

from src.apps.products.converters.products import product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import ProductAuthorPermissionError, ProductNotFoundError
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.use_cases.products.get_by_id import GetProductByIdUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory


@pytest.fixture
def get_product_by_id_use_case(container: Container) -> GetProductByIdUseCase:
    return container.resolve(GetProductByIdUseCase)


@pytest.mark.django_db
def test_visible_product_retrieved_by_anonymous_user(
    product: Product, get_product_by_id_use_case: GetProductByIdUseCase
):
    retrieved_product = get_product_by_id_use_case.execute(seller=None, product_id=product.pk)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product


@pytest.mark.django_db
def test_visible_product_retrieved_by_authorized_user_with_seller_profile(
    seller: Seller, product: Product, get_product_by_id_use_case: GetProductByIdUseCase
):
    retrieved_product = get_product_by_id_use_case.execute(seller=seller_to_entity(dto=seller), product_id=product.pk)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product


@pytest.mark.django_db
def test_not_visible_product_not_retrieved_by_anonymous_user(get_product_by_id_use_case: GetProductByIdUseCase):
    product = ProductModelFactory.create(is_visible=False)
    with pytest.raises(ProductAuthorPermissionError):
        get_product_by_id_use_case.execute(seller=None, product_id=product.pk)


@pytest.mark.django_db
def test_not_visible_product_not_retrieved(seller: Seller, get_product_by_id_use_case: GetProductByIdUseCase):
    product = ProductModelFactory.create(is_visible=False)
    with pytest.raises(ProductAuthorPermissionError):
        get_product_by_id_use_case.execute(seller=seller_to_entity(dto=seller), product_id=product.pk)


@pytest.mark.django_db
def test_not_visible_product_retrieved_by_author(seller: Seller, get_product_by_id_use_case: GetProductByIdUseCase):
    product = ProductModelFactory.create(is_visible=False, seller=seller)
    retrieved_product = get_product_by_id_use_case.execute(seller=seller_to_entity(dto=seller), product_id=product.pk)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product


@pytest.mark.django_db
def test_product_retrieved_with_relations(product: Product, get_product_by_id_use_case: GetProductByIdUseCase):
    expected_variants = 7
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    retrieved_product = get_product_by_id_use_case.execute(seller=None, product_id=product.pk)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert retrieved_product.seller == seller_to_entity(dto=product.seller)
    assert len(retrieved_product.variants) == expected_variants
    assert product_to_entity(dto=db_product) == retrieved_product


@pytest.mark.django_db
def test_product_retrieved_with_relations_and_zero_price(
    product: Product, get_product_by_id_use_case: GetProductByIdUseCase
):
    expected_variants = 7
    expected_variants_with_zero_price = 2
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_variants_with_zero_price, product=product, price=0)
    retrieved_product = get_product_by_id_use_case.execute(seller=None, product_id=product.pk)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert retrieved_product.seller == seller_to_entity(dto=product.seller)
    assert len(retrieved_product.variants) == expected_variants
    assert product_to_entity(dto=db_product) == retrieved_product


@pytest.mark.django_db
def test_product_retrieved_with_relations_and_not_visible_variants(
    product: Product, get_product_by_id_use_case: GetProductByIdUseCase
):
    expected_variants = 2
    expected_not_visible_variants = 6
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    retrieved_product = get_product_by_id_use_case.execute(seller=None, product_id=product.pk)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert retrieved_product.seller == seller_to_entity(dto=product.seller)
    assert len(retrieved_product.variants) == expected_variants
    assert product_to_entity(dto=db_product) == retrieved_product


@pytest.mark.django_db
def test_product_not_retrieved_if_not_exists(get_product_by_id_use_case: GetProductByIdUseCase):
    with pytest.raises(ProductNotFoundError):
        get_product_by_id_use_case.execute(seller=None, product_id=uuid7())
