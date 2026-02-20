from uuid import uuid7

import pytest
from django.db.models import Prefetch
from punq import Container

from src.apps.products.commands.products import GetProductByIdCommand
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.products import ProductAccessForbiddenError, ProductNotFoundByIdError
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.use_cases.products.get_by_id import GetProductByIdUseCase
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def get_product_by_id_use_case(container: Container) -> GetProductByIdUseCase:
    return container.resolve(GetProductByIdUseCase)


@pytest.mark.django_db
def test_get_visible_product_retrieved_by_anonymous_user(
    product: Product, get_product_by_id_use_case: GetProductByIdUseCase
):
    command = GetProductByIdCommand(user_id=None, product_id=product.pk)
    retrieved_product = get_product_by_id_use_case.execute(command=command)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert retrieved_product.seller == seller_to_entity(dto=db_product.seller)
    assert len(retrieved_product.variants) == 0
    assert db_product.id == retrieved_product.id
    assert db_product.slug == retrieved_product.slug
    assert db_product.seller_id == retrieved_product.seller_id
    assert db_product.title == retrieved_product.title
    assert db_product.description == retrieved_product.description
    assert db_product.short_description == retrieved_product.short_description
    assert db_product.is_visible == retrieved_product.is_visible
    assert db_product.created_at == retrieved_product.created_at
    assert db_product.updated_at == retrieved_product.updated_at
    assert db_product.reviews_count == retrieved_product.reviews_count
    assert db_product.reviews_avg_rating == retrieved_product.reviews_avg_rating


@pytest.mark.django_db
def test_get_visible_product_retrieved_by_authorized_user_with_seller_profile(
    seller: Seller, product: Product, get_product_by_id_use_case: GetProductByIdUseCase
):
    command = GetProductByIdCommand(user_id=seller.user_id, product_id=product.pk)
    retrieved_product = get_product_by_id_use_case.execute(command=command)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert retrieved_product.seller == seller_to_entity(dto=db_product.seller)
    assert len(retrieved_product.variants) == 0
    assert db_product.id == retrieved_product.id
    assert db_product.slug == retrieved_product.slug
    assert db_product.seller_id == retrieved_product.seller_id
    assert db_product.title == retrieved_product.title
    assert db_product.description == retrieved_product.description
    assert db_product.short_description == retrieved_product.short_description
    assert db_product.is_visible == retrieved_product.is_visible
    assert db_product.created_at == retrieved_product.created_at
    assert db_product.updated_at == retrieved_product.updated_at
    assert db_product.reviews_count == retrieved_product.reviews_count
    assert db_product.reviews_avg_rating == retrieved_product.reviews_avg_rating


@pytest.mark.django_db
def test_get_invisible_product_not_retrieved_by_anonymous_user_and_access_error_raised(
    get_product_by_id_use_case: GetProductByIdUseCase,
):
    product = ProductModelFactory.create(is_visible=False)
    command = GetProductByIdCommand(user_id=None, product_id=product.pk)
    with pytest.raises(ProductAccessForbiddenError):
        get_product_by_id_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_invisible_product_not_retrieved_by_authorized_user_and_access_error_raised(
    seller: Seller, get_product_by_id_use_case: GetProductByIdUseCase
):
    product = ProductModelFactory.create(is_visible=False)
    command = GetProductByIdCommand(user_id=seller.user_id, product_id=product.pk)
    with pytest.raises(ProductAccessForbiddenError):
        get_product_by_id_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_invisible_product_not_retrieved_by_user_without_seller_profile_and_access_error_raised(
    user: User, get_product_by_id_use_case: GetProductByIdUseCase
):
    product = ProductModelFactory.create(is_visible=False)
    command = GetProductByIdCommand(user_id=user.pk, product_id=product.pk)
    with pytest.raises(ProductAccessForbiddenError):
        get_product_by_id_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_invisible_product_retrieved_by_author(seller: Seller, get_product_by_id_use_case: GetProductByIdUseCase):
    product = ProductModelFactory.create(is_visible=False, seller=seller)
    command = GetProductByIdCommand(user_id=seller.user_id, product_id=product.pk)
    retrieved_product = get_product_by_id_use_case.execute(command=command)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert retrieved_product.seller == seller_to_entity(dto=db_product.seller)
    assert len(retrieved_product.variants) == 0
    assert db_product.id == retrieved_product.id
    assert db_product.slug == retrieved_product.slug
    assert db_product.seller_id == retrieved_product.seller_id
    assert db_product.title == retrieved_product.title
    assert db_product.description == retrieved_product.description
    assert db_product.short_description == retrieved_product.short_description
    assert db_product.is_visible == retrieved_product.is_visible
    assert db_product.created_at == retrieved_product.created_at
    assert db_product.updated_at == retrieved_product.updated_at
    assert db_product.reviews_count == retrieved_product.reviews_count
    assert db_product.reviews_avg_rating == retrieved_product.reviews_avg_rating


@pytest.mark.django_db
def test_get_invisible_product_retrieved_with_correct_relations(
    product: Product, get_product_by_id_use_case: GetProductByIdUseCase
):
    expected_variants = 7
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    command = GetProductByIdCommand(user_id=None, product_id=product.pk)
    retrieved_product = get_product_by_id_use_case.execute(command=command)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert retrieved_product.seller == seller_to_entity(dto=product.seller)
    assert len(retrieved_product.variants) == expected_variants
    assert db_product.id == retrieved_product.id
    assert db_product.slug == retrieved_product.slug
    assert db_product.seller_id == retrieved_product.seller_id
    assert db_product.title == retrieved_product.title
    assert db_product.description == retrieved_product.description
    assert db_product.short_description == retrieved_product.short_description
    assert db_product.is_visible == retrieved_product.is_visible
    assert db_product.created_at == retrieved_product.created_at
    assert db_product.updated_at == retrieved_product.updated_at
    assert db_product.reviews_count == retrieved_product.reviews_count
    assert db_product.reviews_avg_rating == retrieved_product.reviews_avg_rating


@pytest.mark.django_db
def test_get_invisible_product_retrieved_with_correct_relations_and_invisible_variants_are_excluded(
    product: Product, get_product_by_id_use_case: GetProductByIdUseCase
):
    expected_variants = 2
    expected_not_visible_variants = 6
    ProductVariantModelFactory.create_batch(size=expected_variants, product=product)
    ProductVariantModelFactory.create_batch(size=expected_not_visible_variants, product=product, is_visible=False)
    command = GetProductByIdCommand(user_id=None, product_id=product.pk)
    retrieved_product = get_product_by_id_use_case.execute(command=command)
    db_product = (
        Product.objects.filter(pk=product.pk)
        .prefetch_related(Prefetch('variants', ProductVariant.objects.filter(is_visible=True, price__gt=0)))
        .select_related('seller')
        .first()
    )

    assert isinstance(retrieved_product, ProductEntity)
    assert retrieved_product.seller == seller_to_entity(dto=product.seller)
    assert len(retrieved_product.variants) == expected_variants
    assert db_product.id == retrieved_product.id
    assert db_product.slug == retrieved_product.slug
    assert db_product.seller_id == retrieved_product.seller_id
    assert db_product.title == retrieved_product.title
    assert db_product.description == retrieved_product.description
    assert db_product.short_description == retrieved_product.short_description
    assert db_product.is_visible == retrieved_product.is_visible
    assert db_product.created_at == retrieved_product.created_at
    assert db_product.updated_at == retrieved_product.updated_at
    assert db_product.reviews_count == retrieved_product.reviews_count
    assert db_product.reviews_avg_rating == retrieved_product.reviews_avg_rating


@pytest.mark.django_db
def test_get_product_not_found_by_id_error_raised(get_product_by_id_use_case: GetProductByIdUseCase):
    with pytest.raises(ProductNotFoundByIdError):
        command = GetProductByIdCommand(user_id=None, product_id=uuid7())
        get_product_by_id_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_product_user_not_found_error_raised(get_product_by_id_use_case: GetProductByIdUseCase):
    product = ProductModelFactory.create(is_visible=False)
    with pytest.raises(UserNotFoundError):
        command = GetProductByIdCommand(user_id=1, product_id=product.pk)
        get_product_by_id_use_case.execute(command=command)


@pytest.mark.django_db
def test_get_product_user_not_active_error_raised(get_product_by_id_use_case: GetProductByIdUseCase):
    user = UserModelFactory.create(is_active=False)
    product = ProductModelFactory.create(is_visible=False)
    with pytest.raises(UserNotActiveError):
        command = GetProductByIdCommand(user_id=user.pk, product_id=product.pk)
        get_product_by_id_use_case.execute(command=command)
