import pytest
from punq import Container

from src.apps.products.converters.products import product_to_entity
from src.apps.products.exceptions.product_variants import ProductVariantsNotFoundError
from src.apps.products.models.products import Product
from src.apps.products.services.products import BaseProductHasVariantsValidatorService


@pytest.fixture
def product_has_variants_validator_service(container: Container) -> BaseProductHasVariantsValidatorService:
    return container.resolve(BaseProductHasVariantsValidatorService)


@pytest.mark.django_db
def test_validator_error_raised_if_variants_count_equals_zero(
    product_has_variants_validator_service: BaseProductHasVariantsValidatorService,
    product: Product,
):
    product_entity = product_to_entity(dto=product)
    product_entity.variants_count = 0
    with pytest.raises(ProductVariantsNotFoundError):
        product_has_variants_validator_service.validate(product=product_entity)


@pytest.mark.django_db
def test_validator_error_not_raised_if_variants_count_equals_none(
    product_has_variants_validator_service: BaseProductHasVariantsValidatorService,
    product: Product,
):
    product_entity = product_to_entity(dto=product)
    product_entity.variants_count = None
    product_has_variants_validator_service.validate(product=product_entity)


@pytest.mark.django_db
def test_validator_error_not_raised_if_variants_count_greater_than_0(
    product_has_variants_validator_service: BaseProductHasVariantsValidatorService,
    product: Product,
):
    product_entity = product_to_entity(dto=product)
    product_entity.variants_count = 5
    product_has_variants_validator_service.validate(product=product_entity)
