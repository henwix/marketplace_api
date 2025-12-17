from decimal import Decimal
from uuid import uuid7

import pytest

from src.apps.products.models.products import Product
from src.apps.products.repositories.products import BaseProductRepository
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
from tests.v1.products.test_data.new_product_data import PRODUCT_ARGNAMES, PRODUCT_ARGVALUES
from tests.v1.products.utils import create_test_products_with_variant
from tests.v1.sellers.factories import SellerModelFactory


@pytest.mark.django_db
def test_product_saved_for_creation(product_repository: BaseProductRepository):
    product = ProductModelFactory.build(seller=SellerModelFactory.create())
    assert not Product.objects.filter(pk=product.pk).exists()

    saved_product = product_repository.save(product=product, update=False)
    assert isinstance(saved_product, Product)
    assert saved_product == product
    assert Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_ARGNAMES, argvalues=PRODUCT_ARGVALUES)
def test_product_saved_for_update(
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
    assert isinstance(saved_product, Product)
    db_product = Product.objects.get(pk=product.pk)
    assert saved_product == db_product


@pytest.mark.django_db
def test_product_selected_for_update_by_id(product: Product, product_repository: BaseProductRepository):
    retrieved_product = product_repository.select_for_update_by_id_or_none(id=product.pk)
    assert isinstance(retrieved_product, Product)
    assert product == retrieved_product


@pytest.mark.django_db
def test_product_not_selected_for_update_by_id_if_not_exists(product_repository: BaseProductRepository):
    retrieved_product = product_repository.select_for_update_by_id_or_none(id=uuid7())
    assert retrieved_product is None


@pytest.mark.django_db
def test_product_retrieved_by_id(product: Product, product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_by_id_or_none(id=product.pk)
    assert isinstance(retrieved_product, Product)
    assert product == retrieved_product


@pytest.mark.django_db
def test_product_not_retrieved_by_id_if_not_exists(product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_by_id_or_none(id=uuid7())
    assert retrieved_product is None


@pytest.mark.django_db
def test_product_retrieved_by_id_with_relations(product: Product, product_repository: BaseProductRepository):
    expected_variants = 7
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    retrieved_product = product_repository.get_by_id_for_retrieve_or_none(id=product.pk)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert retrieved_product._state.fields_cache.get('seller') == product.seller
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_product_retrieved_by_id_with_relations_and_zero_price(
    product: Product, product_repository: BaseProductRepository
):
    expected_variants = 4
    expected_variants_with_zero_price = 2
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_variants_with_zero_price, product=product, price=0)
    retrieved_product = product_repository.get_by_id_for_retrieve_or_none(id=product.pk)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_product_retrieved_by_id_with_relations_and_not_visible_variants(
    product: Product, product_repository: BaseProductRepository
):
    expected_variants = 2
    expected_not_visible_variants = 6
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    retrieved_product = product_repository.get_by_id_for_retrieve_or_none(id=product.pk)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_product_not_retrieved_by_id_with_relations_if_not_exists(product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_by_id_for_retrieve_or_none(id=uuid7())
    assert retrieved_product is None


@pytest.mark.django_db
def test_product_retrieved_by_slug_with_relations(product: Product, product_repository: BaseProductRepository):
    expected_variants = 2
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    retrieved_product = product_repository.get_by_slug_for_retrieve_or_none(slug=product.slug)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert retrieved_product._state.fields_cache.get('seller') == product.seller
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_product_retrieved_by_slug_with_relations_and_zero_price(
    product: Product, product_repository: BaseProductRepository
):
    expected_variants = 7
    expected_variants_with_zero_price = 3
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_variants_with_zero_price, product=product, price=0)
    retrieved_product = product_repository.get_by_slug_for_retrieve_or_none(slug=product.slug)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_product_retrieved_by_slug_with_relations_and_not_visible_variants(
    product: Product, product_repository: BaseProductRepository
):
    expected_variants = 8
    expected_not_visible_variants = 1
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    retrieved_product = product_repository.get_by_slug_for_retrieve_or_none(slug=product.slug)

    assert isinstance(retrieved_product, Product)
    assert retrieved_product == product
    assert len(getattr(retrieved_product, '_prefetched_objects_cache', {}).get('variants')) == expected_variants


@pytest.mark.django_db
def test_product_not_retrieved_by_slug_with_relations_if_not_exists(product_repository: BaseProductRepository):
    retrieved_product = product_repository.get_by_slug_for_retrieve_or_none(slug='test-slug')
    assert retrieved_product is None


@pytest.mark.django_db
def test_product_deleted(product: Product, product_repository: BaseProductRepository):
    assert Product.objects.filter(pk=product.pk).exists()
    product_repository.delete(id=product.pk)
    assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_products_for_global_search_retrieved(product_repository: BaseProductRepository):
    expected_products = 6
    create_test_products_with_variant({'size': expected_products})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_products


@pytest.mark.django_db
def test_products_for_global_search_not_retrieved_if_product_not_visible(product_repository: BaseProductRepository):
    expected_products = 7
    create_test_products_with_variant({'size': expected_products, 'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == 0


@pytest.mark.django_db
def test_products_for_global_search_not_retrieved_if_variants_not_visible(product_repository: BaseProductRepository):
    expected_products = 7
    create_test_products_with_variant({'size': expected_products}, {'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == 0


@pytest.mark.django_db
def test_products_for_global_search_not_retrieved_if_price_equals_zero(product_repository: BaseProductRepository):
    expected_products = 2
    create_test_products_with_variant({'size': expected_products}, {'price': 0})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == 0


@pytest.mark.django_db
def test_products_for_global_search_not_retrieved_if_stock_equals_zero(product_repository: BaseProductRepository):
    expected_products = 5
    create_test_products_with_variant({'size': expected_products}, {'stock': 0})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == 0


@pytest.mark.django_db
def test_products_for_global_search_retrieved_with_not_visible_products(product_repository: BaseProductRepository):
    expected_visible_products = 6
    expected_invisible_products = 3
    create_test_products_with_variant({'size': expected_visible_products})
    create_test_products_with_variant({'size': expected_invisible_products, 'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_visible_products


@pytest.mark.django_db
def test_products_for_global_search_retrieved_with_not_visible_variants(product_repository: BaseProductRepository):
    expected_visible_products = 3
    expected_invisible_products = 9
    create_test_products_with_variant({'size': expected_visible_products})
    create_test_products_with_variant({'size': expected_invisible_products}, {'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_visible_products


@pytest.mark.django_db
def test_products_for_global_search_retrieved_with_prices_equals_zero(product_repository: BaseProductRepository):
    expected_products_with_positive_price = 8
    expected_products_with_zero_price = 6
    create_test_products_with_variant({'size': expected_products_with_positive_price})
    create_test_products_with_variant({'size': expected_products_with_zero_price}, {'price': 0})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_products_with_positive_price


@pytest.mark.django_db
def test_products_for_global_search_retrieved_with_stock_equals_zero(product_repository: BaseProductRepository):
    expected_products_with_positive_stock = 8
    expected_products_with_zero_stock = 6
    create_test_products_with_variant({'size': expected_products_with_positive_stock})
    create_test_products_with_variant({'size': expected_products_with_zero_stock}, {'stock': 0})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_products_with_positive_stock


@pytest.mark.django_db
def test_products_for_global_search_retrieved_with_mixed_prices(product_repository: BaseProductRepository):
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
def test_products_for_global_search_retrieved_with_mixed_stock(product_repository: BaseProductRepository):
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
def test_products_for_global_search_retrieved_with_mixed_visible_variants(product_repository: BaseProductRepository):
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
def test_products_for_global_search_retrieved_with_mixed_visible_products(product_repository: BaseProductRepository):
    expected_visible_products = 6
    expected_invisible_products = 8
    create_test_products_with_variant({'size': expected_visible_products})
    create_test_products_with_variant({'size': expected_invisible_products, 'is_visible': False})
    retrieved_products = product_repository.get_many_for_global_search()
    assert len(retrieved_products) == expected_visible_products


@pytest.mark.django_db
@pytest.mark.parametrize(
    'expected_min_price',
    [Decimal('13'), Decimal('4'), Decimal('8'), Decimal('14'), Decimal('19'), Decimal('125'), Decimal('118')],
)
def test_products_for_global_search_retrieved_with_correct_price(
    product_repository: BaseProductRepository,
    expected_min_price: Decimal,
):
    product = ProductModelFactory.create()
    ProductVariantModelFactory.create(product=product, price=expected_min_price)
    ProductVariantModelFactory.create(product=product, price=Decimal('150'))
    ProductVariantModelFactory.create(product=product, price=Decimal('420'))
    retrieved_products = product_repository.get_many_for_global_search()
    assert retrieved_products[0].price == expected_min_price


@pytest.mark.django_db
def test_products_for_personal_search_retrived_with_not_owned_products(
    seller: Seller, product_repository: BaseProductRepository
):
    expected_owned_products = 8
    expected_not_owned_products = 4
    ProductModelFactory.create_batch(size=expected_owned_products, seller=seller)
    ProductModelFactory.create_batch(size=expected_not_owned_products)
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.id)
    assert len(retrieved_products) == expected_owned_products


@pytest.mark.django_db
def test_products_for_personal_search_retrived_without_variants(
    seller: Seller, product_repository: BaseProductRepository
):
    expected_products = 5
    ProductModelFactory.create_batch(size=expected_products, seller=seller)
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.id)
    assert len(retrieved_products) == expected_products


@pytest.mark.django_db
def test_products_for_personal_search_retrived_if_not_visible(
    seller: Seller, product_repository: BaseProductRepository
):
    expected_visible_products = 9
    expected_not_visible_products = 7
    ProductModelFactory.create_batch(size=expected_visible_products, seller=seller, is_visible=True)
    ProductModelFactory.create_batch(size=expected_not_visible_products, seller=seller, is_visible=False)
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.id)
    assert len(retrieved_products) == expected_visible_products + expected_not_visible_products


@pytest.mark.django_db
@pytest.mark.parametrize(
    'expected_min_price',
    [Decimal('13'), Decimal('72'), Decimal('3'), Decimal('38'), Decimal('84'), Decimal('125'), Decimal('118')],
)
def test_products_for_personal_search_retrieved_with_correct_price(
    seller: Seller,
    product_repository: BaseProductRepository,
    expected_min_price: Decimal,
):
    product = ProductModelFactory.create(seller=seller)
    ProductVariantModelFactory.create(product=product, price=expected_min_price)
    ProductVariantModelFactory.create(product=product, price=Decimal('150'))
    ProductVariantModelFactory.create(product=product, price=Decimal('420'))
    retrieved_products = product_repository.get_many_for_personal_search(seller_id=seller.id)
    assert retrieved_products[0].price == expected_min_price
