from decimal import Decimal
from uuid import uuid7

import pytest
from punq import Container

from src.apps.products.models.products import Product
from src.apps.products.repositories.products import BaseProductRepository
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
from tests.v1.products.test_data.product_data import PRODUCT_ARGNAMES, PRODUCT_ARGVALUES
from tests.v1.products.test_data.product_variants_data import (
    PRODUCT_VARIANTS_PRICES_ARGNAMES,
    PRODUCT_VARIANTS_PRICES_ARGVALUES,
)
from tests.v1.products.utils import create_test_products_with_variant
from tests.v1.sellers.factories import SellerModelFactory


@pytest.fixture
def product_repository(container: Container) -> BaseProductRepository:
    return container.resolve(BaseProductRepository)


@pytest.mark.django_db
def test_save_product_saved_for_creation(product_repository: BaseProductRepository):
    product = ProductModelFactory.build(seller=SellerModelFactory.create())
    assert not Product.objects.filter(pk=product.pk).exists()

    created_product = product_repository.save(product=product, update=False)
    db_product = Product.objects.get(pk=product.pk)

    assert isinstance(created_product, Product)
    assert created_product.pk == product.pk
    assert created_product.slug == db_product.slug
    assert created_product.seller == db_product.seller
    assert created_product.title == db_product.title
    assert created_product.description == db_product.description
    assert created_product.short_description == db_product.short_description
    assert created_product.is_visible == db_product.is_visible
    assert created_product.created_at == db_product.created_at
    assert created_product.updated_at == db_product.updated_at
    assert product.slug == db_product.slug
    assert product.title == db_product.title
    assert product.description == db_product.description
    assert product.short_description == db_product.short_description
    assert product.seller == db_product.seller
    assert product.is_visible == db_product.is_visible


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_ARGNAMES, argvalues=PRODUCT_ARGVALUES)
def test_save_product_saved_for_update(
    product: Product,
    product_repository: BaseProductRepository,
    expected_title: str,
    expected_desc: str,
    expected_short_desc: str,
    expected_is_visible: bool,
):
    product.title = expected_title
    product.description = expected_desc
    product.short_description = expected_short_desc
    product.is_visible = expected_is_visible

    saved_product = product_repository.save(product=product, update=True)
    db_product = Product.objects.get(pk=product.pk)

    assert isinstance(saved_product, Product)
    assert saved_product == db_product
    assert saved_product.slug == db_product.slug
    assert saved_product.seller == db_product.seller
    assert saved_product.title == db_product.title
    assert saved_product.description == db_product.description
    assert saved_product.short_description == db_product.short_description
    assert saved_product.is_visible == db_product.is_visible
    assert product.slug == db_product.slug
    assert product.title == db_product.title
    assert product.description == db_product.description
    assert product.short_description == db_product.short_description
    assert product.seller == db_product.seller
    assert product.is_visible == db_product.is_visible


@pytest.mark.django_db
def test_select_product_for_update_by_id_selected(product: Product, product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_for_update_by_id(id=product.pk)
    assert isinstance(retrieved_product, Product)
    assert product == retrieved_product


@pytest.mark.django_db
def test_select_product_for_update_by_id_not_selected_if_not_exists(product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_for_update_by_id(id=uuid7())
    assert retrieved_product is None


@pytest.mark.django_db
def test_get_product_by_id_retrieved(product: Product, product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_by_id(id=product.pk)
    assert isinstance(retrieved_product, Product)
    assert product == retrieved_product


@pytest.mark.django_db
def test_get_product_by_id_not_retrieved_if_not_exists(product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_by_id(id=uuid7())
    assert retrieved_product is None


@pytest.mark.django_db
def test_get_product_by_id_with_relations_retrieved(product: Product, product_repository: BaseProductRepository):
    expected_variants = 7
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    retrieved_product = product_repository.get_by_id_for_retrieve(id=product.pk)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert retrieved_product._state.fields_cache.get('seller') == product.seller
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_get_product_by_id_with_relations_and_not_visible_variants_retrieved(
    product: Product, product_repository: BaseProductRepository
):
    expected_variants = 2
    expected_not_visible_variants = 6
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    retrieved_product = product_repository.get_by_id_for_retrieve(id=product.pk)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_get_product_by_id_with_relations_not_retrieved_if_not_exists(product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_by_id_for_retrieve(id=uuid7())
    assert retrieved_product is None


@pytest.mark.django_db
def test_get_product_by_slug_with_relations_retrieved(product: Product, product_repository: BaseProductRepository):
    expected_variants = 2
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    retrieved_product = product_repository.get_by_slug_for_retrieve(slug=product.slug)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert retrieved_product._state.fields_cache.get('seller') == product.seller
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_get_product_by_slug_with_relations_and_not_visible_variants_retrieved(
    product: Product, product_repository: BaseProductRepository
):
    expected_variants = 8
    expected_not_visible_variants = 1
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    retrieved_product = product_repository.get_by_slug_for_retrieve(slug=product.slug)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_get_product_by_slug_with_relations_not_retrieved_if_not_exists(product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_by_slug_for_retrieve(slug='test-slug')
    assert retrieved_product is None


@pytest.mark.django_db
def test_delete_product_deleted(product: Product, product_repository: BaseProductRepository):
    assert Product.objects.filter(pk=product.pk).exists()
    product_repository.delete(id=product.pk)
    assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_get_product_by_id_with_loaded_variants_retrieved(product_repository: BaseProductRepository, product: Product):
    expected_visible_variants = 1
    expected_invisible_variants = 2
    expected_positive_stock_variants = 3
    expected_zero_stock_variants = 1
    expected_positive_price_variants = 1
    expected_negative_price_variants = 1
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

    retrieved_product = product_repository.get_by_id_with_loaded_variants(id=product.pk)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product.variants_count == expected_total_variants
    assert 'variants' in getattr(retrieved_product, '_prefetched_objects_cache', {})
    assert retrieved_product.variants.count() == expected_total_variants


@pytest.mark.django_db
def test_get_product_by_id_with_loaded_variants_not_retrieved_if_not_exists(product_repository: BaseProductRepository):
    assert product_repository.get_by_id_with_loaded_variants(id=uuid7()) is None


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved(product_repository: BaseProductRepository):
    expected_products = 6
    create_test_products_with_variant({'size': expected_products})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_products


@pytest.mark.django_db
def test_get_products_for_global_search_not_retrieved_if_product_not_visible(product_repository: BaseProductRepository):
    expected_products = 7
    create_test_products_with_variant({'size': expected_products, 'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == 0


@pytest.mark.django_db
def test_get_products_for_global_search_not_retrieved_if_variants_not_visible(
    product_repository: BaseProductRepository,
):
    expected_products = 7
    create_test_products_with_variant({'size': expected_products}, {'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == 0


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_not_visible_products(product_repository: BaseProductRepository):
    expected_visible_products = 6
    expected_invisible_products = 3
    create_test_products_with_variant({'size': expected_visible_products})
    create_test_products_with_variant({'size': expected_invisible_products, 'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_visible_products


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_not_visible_variants(product_repository: BaseProductRepository):
    expected_visible_products = 3
    expected_invisible_products = 9
    create_test_products_with_variant({'size': expected_visible_products})
    create_test_products_with_variant({'size': expected_invisible_products}, {'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_visible_products


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_stock_equals_zero(product_repository: BaseProductRepository):
    expected_products_with_positive_stock = 8
    expected_products_with_zero_stock = 6
    create_test_products_with_variant({'size': expected_products_with_positive_stock})
    create_test_products_with_variant({'size': expected_products_with_zero_stock}, {'stock': 0})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_products_with_positive_stock


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_mixed_prices(product_repository: BaseProductRepository):
    expected_products = 8
    expected_positive_prices = 5
    expected_zero_prices = 5

    products = ProductModelFactory.create_batch(size=expected_products)
    for product in products:
        ProductVariantModelFactory.create_batch(size=expected_positive_prices, product=product)
        ProductVariantModelFactory.create_batch(size=expected_zero_prices, product=product, price=0)

    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_products


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_mixed_stock(product_repository: BaseProductRepository):
    expected_products = 13
    expected_positive_stock = 5
    expected_zero_stock = 3

    products = ProductModelFactory.create_batch(size=expected_products)
    for product in products:
        ProductVariantModelFactory.create_batch(size=expected_positive_stock, product=product)
        ProductVariantModelFactory.create_batch(size=expected_zero_stock, product=product, stock=0)

    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_products


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_mixed_visible_variants(
    product_repository: BaseProductRepository,
):
    expected_products = 4
    expected_visible_variants = 3
    expected_invisible_variants = 4

    products = ProductModelFactory.create_batch(size=expected_products)
    for product in products:
        ProductVariantModelFactory.create_batch(size=expected_visible_variants, product=product)
        ProductVariantModelFactory.create_batch(size=expected_invisible_variants, product=product, is_visible=False)

    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_products


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_mixed_visible_products(
    product_repository: BaseProductRepository,
):
    expected_visible_products = 6
    expected_invisible_products = 8
    create_test_products_with_variant({'size': expected_visible_products})
    create_test_products_with_variant({'size': expected_invisible_products, 'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_visible_products


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_VARIANTS_PRICES_ARGNAMES, argvalues=PRODUCT_VARIANTS_PRICES_ARGVALUES)
def test_get_products_for_global_search_retrieved_with_correct_min_price_if_all_variants_are_visible(
    product_repository: BaseProductRepository,
    expected_min_price: Decimal,
    expected_first_price: Decimal,
    expected_second_price: Decimal,
):
    product = ProductModelFactory.create()
    ProductVariantModelFactory.create(product=product, price=expected_min_price)
    ProductVariantModelFactory.create(product=product, price=expected_first_price)
    ProductVariantModelFactory.create(product=product, price=expected_second_price)
    retrieved_products = product_repository.get_many_for_global_search()
    assert retrieved_products[0].price == expected_min_price


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_correct_min_price_with_invisible_variants(
    product_repository: BaseProductRepository,
):
    expected_price = Decimal('136')
    product = ProductModelFactory.create()
    ProductVariantModelFactory.create(product=product, price=expected_price)
    ProductVariantModelFactory.create(product=product, price=Decimal('84'), is_visible=False)
    ProductVariantModelFactory.create(product=product, price=Decimal('54'), is_visible=False)
    ProductVariantModelFactory.create(product=product, price=Decimal('31'), is_visible=False)
    ProductVariantModelFactory.create(product=product, price=Decimal('153'))
    retrieved_products = product_repository.get_many_for_global_search()
    assert retrieved_products[0].price == expected_price


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_correct_min_price_with_zero_stock(
    product_repository: BaseProductRepository,
):
    expected_price = Decimal('122')
    product = ProductModelFactory.create()
    ProductVariantModelFactory.create(product=product, price=expected_price)
    ProductVariantModelFactory.create(product=product, price=Decimal('84'), stock=0)
    ProductVariantModelFactory.create(product=product, price=Decimal('12'), stock=0)
    ProductVariantModelFactory.create(product=product, price=Decimal('298'))
    retrieved_products = product_repository.get_many_for_global_search()
    assert retrieved_products[0].price == expected_price


@pytest.mark.django_db
def test_get_products_for_personal_search_retrieved_only_owned_products(
    seller: Seller, product_repository: BaseProductRepository
):
    expected_owned_products = 8
    expected_not_owned_products = 4
    ProductModelFactory.create_batch(size=expected_owned_products, seller=seller)
    ProductModelFactory.create_batch(size=expected_not_owned_products)
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.id)
    assert len(retrieved_products) == expected_owned_products


@pytest.mark.django_db
def test_get_products_for_personal_search_retrieved_without_variants(
    seller: Seller, product_repository: BaseProductRepository
):
    expected_products = 5
    ProductModelFactory.create_batch(size=expected_products, seller=seller)
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.id)
    assert len(retrieved_products) == expected_products


@pytest.mark.django_db
def test_get_products_for_personal_search_retrieved_if_not_visible(
    seller: Seller, product_repository: BaseProductRepository
):
    expected_visible_products = 9
    expected_not_visible_products = 7
    ProductModelFactory.create_batch(size=expected_visible_products, seller=seller, is_visible=True)
    ProductModelFactory.create_batch(size=expected_not_visible_products, seller=seller, is_visible=False)
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.id)
    assert len(retrieved_products) == expected_visible_products + expected_not_visible_products


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_VARIANTS_PRICES_ARGNAMES, argvalues=PRODUCT_VARIANTS_PRICES_ARGVALUES)
def test_get_products_for_personal_search_retrieved_with_correct_min_price_if_all_variants_are_visible(
    seller: Seller,
    product_repository: BaseProductRepository,
    expected_min_price: Decimal,
    expected_first_price: Decimal,
    expected_second_price: Decimal,
):
    product = ProductModelFactory.create(seller=seller)
    ProductVariantModelFactory.create(product=product, price=expected_min_price)
    ProductVariantModelFactory.create(product=product, price=expected_first_price)
    ProductVariantModelFactory.create(product=product, price=expected_second_price)
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.pk)
    assert retrieved_products[0].price == expected_min_price


@pytest.mark.django_db
def test_get_products_for_personal_search_retrieved_with_correct_min_price_with_invisible_variants(
    seller: Seller,
    product_repository: BaseProductRepository,
):
    expected_price = Decimal('136')
    product = ProductModelFactory.create(seller=seller)
    ProductVariantModelFactory.create(product=product, price=expected_price)
    ProductVariantModelFactory.create(product=product, price=Decimal('84'), is_visible=False)
    ProductVariantModelFactory.create(product=product, price=Decimal('54'), is_visible=False)
    ProductVariantModelFactory.create(product=product, price=Decimal('31'), is_visible=False)
    ProductVariantModelFactory.create(product=product, price=Decimal('153'))
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.pk)
    assert retrieved_products[0].price == expected_price


@pytest.mark.django_db
def test_get_products_for_personal_search_retrieved_with_correct_min_price_with_zero_stock(
    seller: Seller,
    product_repository: BaseProductRepository,
):
    expected_price = Decimal('122')
    product = ProductModelFactory.create(seller=seller)
    ProductVariantModelFactory.create(product=product, price=expected_price)
    ProductVariantModelFactory.create(product=product, price=Decimal('84'), stock=0)
    ProductVariantModelFactory.create(product=product, price=Decimal('12'), stock=0)
    ProductVariantModelFactory.create(product=product, price=Decimal('298'))
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.pk)
    assert retrieved_products[0].price == expected_price


@pytest.mark.django_db
def test_get_products_for_global_search_retrieved_with_none_price_if_all_variants_are_invisible(
    seller: Seller,
    product_repository: BaseProductRepository,
):
    product = ProductModelFactory.create(seller=seller)
    ProductVariantModelFactory.create(product=product, price=Decimal('84'), is_visible=False)
    ProductVariantModelFactory.create(product=product, price=Decimal('111'), is_visible=False)
    ProductVariantModelFactory.create(product=product, price=Decimal('3'), is_visible=False)
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.pk)
    assert retrieved_products[0].price is None
