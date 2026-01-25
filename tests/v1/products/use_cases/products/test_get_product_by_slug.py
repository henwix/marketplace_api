import pytest
from django.db.models import Prefetch
from punq import Container

from src.apps.products.commands.products import GetProductBySlugCommand
from src.apps.products.converters.products import product_to_entity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import (
    ProductAccessForbiddenError,
    ProductNotFoundBySlugError,
)
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.use_cases.products.get_by_slug import GetProductBySlugUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def get_product_by_slug_use_case(container: Container) -> GetProductBySlugUseCase:
    return container.resolve(GetProductBySlugUseCase)


@pytest.mark.django_db
def test_get_visible_product_retrieved_by_anonymous_user(
    product: Product, get_product_by_slug_use_case: GetProductBySlugUseCase
):
    command = GetProductBySlugCommand(user_id=None, slug=product.slug)
    retrieved_product = get_product_by_slug_use_case.execute(command=command)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product


@pytest.mark.django_db
def test_get_visible_product_retrieved_by_authorized_user_with_seller_profile(
    seller: Seller, product: Product, get_product_by_slug_use_case: GetProductBySlugUseCase
):
    command = GetProductBySlugCommand(user_id=seller.user_id, slug=product.slug)
    retrieved_product = get_product_by_slug_use_case.execute(command=command)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product


@pytest.mark.django_db
def test_get_invisible_product_not_retrieved_by_anonymous_user_and_access_error_raised(
    get_product_by_slug_use_case: GetProductBySlugUseCase,
):
    product = ProductModelFactory.create(is_visible=False)
    command = GetProductBySlugCommand(user_id=None, slug=product.slug)
    with pytest.raises(ProductAccessForbiddenError):
        get_product_by_slug_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_invisible_product_not_retrieved_by_authorized_user_and_access_error_raised(
    seller: Seller, get_product_by_slug_use_case: GetProductBySlugUseCase
):
    product = ProductModelFactory.create(is_visible=False)
    command = GetProductBySlugCommand(user_id=seller.user_id, slug=product.slug)
    with pytest.raises(ProductAccessForbiddenError):
        get_product_by_slug_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_invisible_product_not_retrieved_by_user_without_seller_profile_and_access_error_raised(
    user: User, get_product_by_slug_use_case: GetProductBySlugUseCase
):
    product = ProductModelFactory.create(is_visible=False)
    command = GetProductBySlugCommand(user_id=user.pk, slug=product.slug)
    with pytest.raises(ProductAccessForbiddenError):
        get_product_by_slug_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_invisible_product_retrieved_by_author(
    seller: Seller, get_product_by_slug_use_case: GetProductBySlugUseCase
):
    product = ProductModelFactory.create(is_visible=False, seller=seller)
    command = GetProductBySlugCommand(user_id=seller.user_id, slug=product.slug)
    retrieved_product = get_product_by_slug_use_case.execute(command=command)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert product_to_entity(dto=db_product) == retrieved_product


@pytest.mark.django_db
def test_get_invisible_product_retrieved_with_correct_relations(
    product: Product, get_product_by_slug_use_case: GetProductBySlugUseCase
):
    expected_variants = 7
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    command = GetProductBySlugCommand(user_id=None, slug=product.slug)
    retrieved_product = get_product_by_slug_use_case.execute(command=command)
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
def test_get_invisible_product_retrieved_with_correct_relations_and_invisible_variants_are_excluded(
    product: Product, get_product_by_slug_use_case: GetProductBySlugUseCase
):
    expected_variants = 2
    expected_not_visible_variants = 6
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    command = GetProductBySlugCommand(user_id=None, slug=product.slug)
    retrieved_product = get_product_by_slug_use_case.execute(command=command)
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
def test_get_product_not_found_by_id_error_raised(get_product_by_slug_use_case: GetProductBySlugUseCase):
    command = GetProductBySlugCommand(user_id=None, slug='test-slug')
    with pytest.raises(ProductNotFoundBySlugError):
        get_product_by_slug_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_product_user_not_found_error_raised(get_product_by_slug_use_case: GetProductBySlugUseCase):
    product = ProductModelFactory.create(is_visible=False)
    command = GetProductBySlugCommand(user_id=1, slug=product.slug)
    with pytest.raises(UserNotFoundError):
        get_product_by_slug_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_product_user_not_active_error_raised(get_product_by_slug_use_case: GetProductBySlugUseCase):
    user = UserModelFactory.create(is_active=False)
    product = ProductModelFactory.create(is_visible=False)
    command = GetProductBySlugCommand(user_id=user.pk, slug=product.slug)
    with pytest.raises(UserNotActiveError):
        get_product_by_slug_use_case.execute(command=command)
