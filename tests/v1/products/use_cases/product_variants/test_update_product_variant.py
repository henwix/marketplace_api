from decimal import Decimal
from uuid import uuid7

import pytest
from punq import Container

from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.exceptions.product_variants import (
    ProductVariantAccessForbiddenError,
    ProductVariantNotFoundError,
)
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.use_cases.product_variants.update import UpdateProductVariantUseCase
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import (
    UserAuthCredentialsNotProvidedError,
    UserAuthNotActiveError,
    UserAuthNotFoundError,
)
from src.apps.users.models import User
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def update_product_variant_use_case(container: Container) -> UpdateProductVariantUseCase:
    return container.resolve(UpdateProductVariantUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames=['expected_title', 'expected_price', 'expected_stock', 'expected_is_visible'],
    argvalues=[
        ('Test Variant Title', Decimal('34.99'), 13, True),
        ('VarriantTitleTest', Decimal('19399.99'), 105, False),
    ],
)
def test_update_variant_updated(
    update_product_variant_use_case: UpdateProductVariantUseCase,
    seller: Seller,
    expected_title: str,
    expected_price: Decimal,
    expected_stock: int,
    expected_is_visible: bool,
):
    expected_data = {
        'title': expected_title,
        'price': expected_price,
        'stock': expected_stock,
        'is_visible': expected_is_visible,
    }
    product = ProductModelFactory.create(seller=seller)
    product_variant = ProductVariantModelFactory.create(product=product)

    updated_product_variant = update_product_variant_use_case.execute(
        user_id=seller.user_id,
        product_variant_id=product_variant.pk,
        data=expected_data,
    )
    db_product_variant = ProductVariant.objects.get(
        pk=product_variant.id,
        title=expected_title,
        price=expected_price,
        stock=expected_stock,
        is_visible=expected_is_visible,
    )
    assert ProductVariant.objects.filter(product_id=product.pk).count() == 1
    assert isinstance(updated_product_variant, ProductVariantEntity)
    assert product_variant_to_entity(dto=db_product_variant) == updated_product_variant


@pytest.mark.django_db
def test_update_variant_product_variant_not_found_error_raised(
    update_product_variant_use_case: UpdateProductVariantUseCase, seller: Seller
):
    with pytest.raises(ProductVariantNotFoundError):
        update_product_variant_use_case.execute(user_id=seller.user_id, product_variant_id=uuid7(), data={})
    assert ProductVariant.objects.all().count() == 0


@pytest.mark.django_db
def test_update_variant_product_access_forbidden_error_raised(
    update_product_variant_use_case: UpdateProductVariantUseCase, seller: Seller, product_variant: ProductVariant
):
    with pytest.raises(ProductVariantAccessForbiddenError):
        update_product_variant_use_case.execute(user_id=seller.user_id, product_variant_id=product_variant.pk, data={})
    assert ProductVariant.objects.all().count() == 1


@pytest.mark.django_db
def test_update_variant_seller_not_found_error_raised(
    update_product_variant_use_case: UpdateProductVariantUseCase,
    user: User,
):
    with pytest.raises(SellerNotFoundError):
        update_product_variant_use_case.execute(user_id=user.pk, product_variant_id=uuid7(), data={})


@pytest.mark.django_db
def test_update_variant_user_credentials_error_raised(update_product_variant_use_case: UpdateProductVariantUseCase):
    with pytest.raises(UserAuthCredentialsNotProvidedError):
        update_product_variant_use_case.execute(user_id=None, product_variant_id=uuid7(), data={})


@pytest.mark.django_db
def test_update_variant_user_not_found_error_raised(update_product_variant_use_case: UpdateProductVariantUseCase):
    with pytest.raises(UserAuthNotFoundError):
        update_product_variant_use_case.execute(user_id=1, product_variant_id=uuid7(), data={})


@pytest.mark.django_db
def test_update_variant_user_not_active_error_raised(update_product_variant_use_case: UpdateProductVariantUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserAuthNotActiveError):
        update_product_variant_use_case.execute(user_id=user.pk, product_variant_id=uuid7(), data={})
