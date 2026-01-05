from uuid import uuid7

import pytest
from punq import Container

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.products.commands.product_variants import DeleteProductVariantCommand
from src.apps.products.exceptions.product_variants import (
    ProductVariantAccessForbiddenError,
    ProductVariantNotFoundError,
)
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.use_cases.product_variants.delete import DeleteProductVariantUseCase
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
def delete_product_variant_use_case(container: Container) -> DeleteProductVariantUseCase:
    return container.resolve(DeleteProductVariantUseCase)


@pytest.mark.django_db
def test_delete_variant_deleted(
    delete_product_variant_use_case: DeleteProductVariantUseCase,
    seller: Seller,
):
    product = ProductModelFactory.create(seller=seller)
    product_variant = ProductVariantModelFactory.create(product=product)

    assert ProductVariant.objects.filter(product_id=product.pk).count() == 1
    command = DeleteProductVariantCommand(user_id=seller.user_id, product_variant_id=product_variant.pk)
    delete_product_variant_use_case.execute(command=command)
    assert ProductVariant.objects.filter(product_id=product.pk).count() == 0


@pytest.mark.django_db
def test_delete_variant_product_variant_not_found_error_raised(
    delete_product_variant_use_case: DeleteProductVariantUseCase, seller: Seller
):
    with pytest.raises(ProductVariantNotFoundError):
        command = DeleteProductVariantCommand(user_id=seller.user_id, product_variant_id=uuid7())
        delete_product_variant_use_case.execute(command=command)
    assert ProductVariant.objects.all().count() == 0


@pytest.mark.django_db
def test_delete_variant_product_access_forbidden_error_raised(
    delete_product_variant_use_case: DeleteProductVariantUseCase, seller: Seller, product_variant: ProductVariant
):
    with pytest.raises(ProductVariantAccessForbiddenError):
        command = DeleteProductVariantCommand(user_id=seller.user_id, product_variant_id=product_variant.pk)
        delete_product_variant_use_case.execute(command=command)
    assert ProductVariant.objects.all().count() == 1


@pytest.mark.django_db
def test_delete_variant_seller_not_found_error_raised(
    delete_product_variant_use_case: DeleteProductVariantUseCase,
    user: User,
):
    with pytest.raises(SellerNotFoundError):
        command = DeleteProductVariantCommand(user_id=user.pk, product_variant_id=uuid7())
        delete_product_variant_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_variant_user_credentials_error_raised(delete_product_variant_use_case: DeleteProductVariantUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        command = DeleteProductVariantCommand(user_id=None, product_variant_id=uuid7())
        delete_product_variant_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_variant_user_not_found_error_raised(delete_product_variant_use_case: DeleteProductVariantUseCase):
    with pytest.raises(UserNotFoundError):
        command = DeleteProductVariantCommand(user_id=1, product_variant_id=uuid7())
        delete_product_variant_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_variant_user_not_active_error_raised(delete_product_variant_use_case: DeleteProductVariantUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        command = DeleteProductVariantCommand(user_id=user.pk, product_variant_id=uuid7())
        delete_product_variant_use_case.execute(command=command)
