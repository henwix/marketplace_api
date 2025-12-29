import pytest
from punq import Container

from src.apps.products.converters.products import product_to_entity
from src.apps.products.exceptions.product_variants import ProductVariantsLimitError
from src.apps.products.models.products import Product
from src.apps.products.services.products import BaseProductVariantsLimitValidatorService
from tests.v1.products.factories import ProductVariantModelFactory


@pytest.fixture
def product_variants_limit_validator_service(container: Container) -> BaseProductVariantsLimitValidatorService:
    return container.resolve(BaseProductVariantsLimitValidatorService)


@pytest.mark.django_db
@pytest.mark.parametrize('expected_products', [10, 11, 12])
def test_validator_error_raised_if_limit_reached(
    product_variants_limit_validator_service: BaseProductVariantsLimitValidatorService,
    product: Product,
    expected_products: int,
):
    ProductVariantModelFactory.create_batch(size=expected_products, product=product)
    with pytest.raises(ProductVariantsLimitError):
        product_variants_limit_validator_service.validate(product=product_to_entity(dto=product))


@pytest.mark.django_db
@pytest.mark.parametrize('expected_products', [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_validator_error_not_raised_if_validated(
    product_variants_limit_validator_service: BaseProductVariantsLimitValidatorService,
    product: Product,
    expected_products: int,
):
    ProductVariantModelFactory.create_batch(size=expected_products, product=product)
    product_variants_limit_validator_service.validate(product=product_to_entity(dto=product))
