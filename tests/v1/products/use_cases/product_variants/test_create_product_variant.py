from decimal import Decimal
from uuid import uuid7

import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.products.commands.product_variants import CreateProductVariantCommand
from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.exceptions.product_variants import ProductVariantsLimitError
from src.apps.products.exceptions.products import ProductAccessForbiddenError, ProductNotFoundByIdError
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.use_cases.product_variants.create import CreateProductVariantUseCase
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
)
from src.apps.users.models import User
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def create_product_variant_use_case(container: Container) -> CreateProductVariantUseCase:
    return container.resolve(CreateProductVariantUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames=['expected_title', 'expected_price', 'expected_stock', 'expected_is_visible'],
    argvalues=[
        ('Test Variant Title', Decimal('34.99'), 13, True),
        ('VarriantTitleTest', Decimal('19399.99'), 105, False),
    ],
)
def test_create_variant_created(
    create_product_variant_use_case: CreateProductVariantUseCase,
    seller: Seller,
    expected_title: str,
    expected_price: Decimal,
    expected_stock: int,
    expected_is_visible: bool,
):
    product = ProductModelFactory.create(seller=seller)
    assert ProductVariant.objects.filter(product_id=product.pk).count() == 0

    command = CreateProductVariantCommand(
        user_id=seller.user_id,
        product_id=product.pk,
        title=expected_title,
        price=expected_price,
        stock=expected_stock,
        is_visible=expected_is_visible,
    )
    created_product_variant = create_product_variant_use_case.execute(command=command)
    db_product_variant = ProductVariant.objects.get(
        pk=created_product_variant.id,
        title=expected_title,
        price=expected_price,
        stock=expected_stock,
        is_visible=expected_is_visible,
    )
    assert ProductVariant.objects.filter(product_id=product.pk).count() == 1
    assert isinstance(created_product_variant, ProductVariantEntity)
    assert product_variant_to_entity(dto=db_product_variant) == created_product_variant


@pytest.mark.django_db
def test_create_variant_product_not_found_error_raised(
    create_product_variant_use_case: CreateProductVariantUseCase, seller: Seller
):
    with pytest.raises(ProductNotFoundByIdError):
        command = CreateProductVariantCommand(
            user_id=seller.user_id,
            product_id=uuid7(),
            title='1',
            price=Decimal('1'),
            stock=0,
            is_visible=True,
        )
        create_product_variant_use_case.execute(command=command)
    assert ProductVariant.objects.all().count() == 0


@pytest.mark.django_db
def test_create_variant_not_created_and_product_access_error_raised(
    create_product_variant_use_case: CreateProductVariantUseCase, seller: Seller, product: Product
):
    with pytest.raises(ProductAccessForbiddenError):
        command = CreateProductVariantCommand(
            user_id=seller.user_id,
            product_id=product.pk,
            title='1',
            price=Decimal('1'),
            stock=0,
            is_visible=True,
        )
        create_product_variant_use_case.execute(command=command)
    assert ProductVariant.objects.all().count() == 0


@pytest.mark.django_db
def test_create_variant_not_created_and_variants_limit_error_raised(
    create_product_variant_use_case: CreateProductVariantUseCase, seller: Seller
):
    product = ProductModelFactory.create(seller=seller)
    ProductVariantModelFactory.create_batch(size=10, product=product)
    assert ProductVariant.objects.all().count() == 10
    with pytest.raises(ProductVariantsLimitError):
        command = CreateProductVariantCommand(
            user_id=seller.user_id,
            product_id=product.pk,
            title='1',
            price=Decimal('1'),
            stock=0,
            is_visible=True,
        )
        create_product_variant_use_case.execute(command=command)
    assert ProductVariant.objects.all().count() == 10


@pytest.mark.django_db
def test_create_variant_seller_not_found_error_raised(
    create_product_variant_use_case: CreateProductVariantUseCase,
    user: User,
):
    with pytest.raises(SellerNotFoundError):
        command = CreateProductVariantCommand(
            user_id=user.pk,
            product_id=uuid7(),
            title='1',
            price=Decimal('1'),
            stock=0,
            is_visible=True,
        )
        create_product_variant_use_case.execute(command=command)


@pytest.mark.django_db
def test_create_variant_user_credentials_error_raised(create_product_variant_use_case: CreateProductVariantUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        command = CreateProductVariantCommand(
            user_id=None,
            product_id=uuid7(),
            title='1',
            price=Decimal('1'),
            stock=0,
            is_visible=True,
        )
        create_product_variant_use_case.execute(command=command)


@pytest.mark.django_db
def test_create_variant_user_not_found_error_raised(create_product_variant_use_case: CreateProductVariantUseCase):
    with pytest.raises(UserNotFoundError):
        command = CreateProductVariantCommand(
            user_id=1,
            product_id=uuid7(),
            title='1',
            price=Decimal('1'),
            stock=0,
            is_visible=True,
        )
        create_product_variant_use_case.execute(command=command)


@pytest.mark.django_db
def test_create_variant_user_not_active_error_raised(create_product_variant_use_case: CreateProductVariantUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        command = CreateProductVariantCommand(
            user_id=user.pk,
            product_id=uuid7(),
            title='1',
            price=Decimal('1'),
            stock=0,
            is_visible=True,
        )
        create_product_variant_use_case.execute(command=command)
