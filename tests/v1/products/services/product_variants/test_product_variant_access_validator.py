import pytest
from punq import Container

from src.apps.products.converters.product_variants import product_variant_to_entity
from src.apps.products.exceptions.product_variants import ProductVariantAccessForbiddenError
from src.apps.products.models.product_variants import ProductVariant
from src.apps.products.services.product_variants import BaseProductVariantAccessValidatorService
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory


@pytest.fixture
def variant_access_validator_service(container: Container) -> BaseProductVariantAccessValidatorService:
    return container.resolve(BaseProductVariantAccessValidatorService)


@pytest.mark.django_db
def test_validator_exception_raised_if_seller_is_none(
    variant_access_validator_service: BaseProductVariantAccessValidatorService,
    product_variant: ProductVariant,
):
    with pytest.raises(ProductVariantAccessForbiddenError):
        variant_access_validator_service.validate(
            seller=None, product_variant=product_variant_to_entity(dto=product_variant)
        )


@pytest.mark.django_db
def test_validator_exception_raised_if_seller_is_not_author(
    variant_access_validator_service: BaseProductVariantAccessValidatorService,
    seller: Seller,
    product_variant: ProductVariant,
):
    with pytest.raises(ProductVariantAccessForbiddenError):
        variant_access_validator_service.validate(
            seller=seller_to_entity(dto=seller), product_variant=product_variant_to_entity(dto=product_variant)
        )


@pytest.mark.django_db
def test_validator_exception_not_raised_if_validated(
    variant_access_validator_service: BaseProductVariantAccessValidatorService,
    seller: Seller,
):
    product = ProductModelFactory.create(seller=seller)
    product_variant = ProductVariantModelFactory.create(product=product)
    variant_access_validator_service.validate(
        seller=seller_to_entity(dto=seller), product_variant=product_variant_to_entity(dto=product_variant)
    )
