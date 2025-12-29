from uuid import uuid7

import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.products.entities.product_variants import ProductVariantEntity
from src.apps.products.exceptions.product_variants import ProductVariantsNotFoundError
from src.apps.products.exceptions.products import ProductAccessForbiddenError, ProductNotFoundByIdError
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.models.products import Product
from src.apps.products.use_cases.product_variants.get import GetProductVariantsUseCase
from src.apps.sellers.exceptions import SellerNotFoundError
from src.apps.sellers.models import Seller
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory
from tests.v1.users.factories import UserModelFactory


@pytest.fixture
def get_product_variants_use_case(container: Container) -> GetProductVariantsUseCase:
    return container.resolve(GetProductVariantsUseCase)


@pytest.mark.django_db
@pytest.mark.parametrize('expected_variants_count', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_get_product_variants_retrieved(
    get_product_variants_use_case: GetProductVariantsUseCase,
    seller: Seller,
    expected_variants_count: int,
):
    product = ProductModelFactory.create(seller=seller)
    ProductVariantModelFactory.create_batch(size=expected_variants_count, product=product)

    variants_count, variants = get_product_variants_use_case.execute(user_id=seller.user_id, product_id=product.pk)

    assert ProductVariant.objects.filter(product_id=product.pk).count() == expected_variants_count
    assert variants_count == expected_variants_count
    assert len(variants) == expected_variants_count
    for variant in variants:
        assert isinstance(variant, ProductVariantEntity)


@pytest.mark.django_db
def test_get_product_variants_product_not_found_error_raised(
    get_product_variants_use_case: GetProductVariantsUseCase,
    seller: Seller,
):
    with pytest.raises(ProductNotFoundByIdError):
        get_product_variants_use_case.execute(user_id=seller.user_id, product_id=uuid7())
    assert ProductVariant.objects.all().count() == 0


@pytest.mark.django_db
def test_get_product_variants_variants_not_found_error_raised(
    get_product_variants_use_case: GetProductVariantsUseCase,
    seller: Seller,
):
    product = ProductModelFactory.create(seller=seller)
    with pytest.raises(ProductVariantsNotFoundError):
        get_product_variants_use_case.execute(user_id=seller.user_id, product_id=product.pk)
    assert ProductVariant.objects.filter(product=product).count() == 0


@pytest.mark.django_db
def test_get_product_variants_product_access_forbidden_error_raised(
    get_product_variants_use_case: GetProductVariantsUseCase,
    seller: Seller,
    product: Product,
):
    with pytest.raises(ProductAccessForbiddenError):
        get_product_variants_use_case.execute(user_id=seller.user_id, product_id=product.pk)


@pytest.mark.django_db
def test_get_product_variants_seller_not_found_error_raised(
    get_product_variants_use_case: GetProductVariantsUseCase,
    user: User,
):
    with pytest.raises(SellerNotFoundError):
        get_product_variants_use_case.execute(user_id=user.pk, product_id=uuid7())


@pytest.mark.django_db
def test_get_priduct_variants_user_credentials_error_raised(get_product_variants_use_case: GetProductVariantsUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        get_product_variants_use_case.execute(user_id=None, product_id=uuid7())


@pytest.mark.django_db
def test_get_product_variants_user_not_found_error_raised(get_product_variants_use_case: GetProductVariantsUseCase):
    with pytest.raises(UserNotFoundError):
        get_product_variants_use_case.execute(user_id=1, product_id=uuid7())


@pytest.mark.django_db
def test_get_product_variants_user_not_active_error_raised(get_product_variants_use_case: GetProductVariantsUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        get_product_variants_use_case.execute(user_id=user.pk, product_id=uuid7())
