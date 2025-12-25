import pytest

from src.apps.products.converters.products import product_to_entity
from src.apps.products.exceptions.products import ProductAccessForbiddenError
from src.apps.products.models.products import Product
from src.apps.products.services.products import BaseProductAuthorValidatorService
from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.sellers.models import Seller
from tests.v1.products.factories import ProductModelFactory


@pytest.mark.django_db
def test_validator_exception_raised_if_seller_is_none(
    product_author_validator_service: BaseProductAuthorValidatorService,
    product: Product,
):
    with pytest.raises(ProductAccessForbiddenError):
        product_author_validator_service.validate(seller=None, product=product_to_entity(dto=product))


@pytest.mark.django_db
def test_validator_exception_raised_if_seller_is_not_author(
    product_author_validator_service: BaseProductAuthorValidatorService,
    seller: Seller,
    product: Product,
):
    with pytest.raises(ProductAccessForbiddenError):
        product_author_validator_service.validate(
            seller=seller_to_entity(dto=seller), product=product_to_entity(dto=product)
        )


@pytest.mark.django_db
def test_validator_exception_not_raised_if_validated(
    product_author_validator_service: BaseProductAuthorValidatorService,
    seller: Seller,
):
    product = ProductModelFactory.create(seller=seller)
    product_author_validator_service.validate(
        seller=seller_to_entity(dto=seller), product=product_to_entity(dto=product)
    )
