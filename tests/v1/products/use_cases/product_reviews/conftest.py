import pytest
from punq import Container

from src.apps.products.use_cases.product_reviews.create import CreateProductReviewUseCase
from src.apps.products.use_cases.product_reviews.delete import DeleteProductReviewUseCase
from src.apps.products.use_cases.product_reviews.get import GetProductReviewsUseCase
from src.apps.products.use_cases.product_reviews.update import UpdateProductReviewUseCase


@pytest.fixture
def create_product_review_use_case(container: Container) -> CreateProductReviewUseCase:
    return container.resolve(CreateProductReviewUseCase)


@pytest.fixture
def delete_product_review_use_case(container: Container) -> DeleteProductReviewUseCase:
    return container.resolve(DeleteProductReviewUseCase)


@pytest.fixture
def get_product_reviews_use_case(container: Container) -> GetProductReviewsUseCase:
    return container.resolve(GetProductReviewsUseCase)


@pytest.fixture
def update_product_review_use_case(container: Container) -> UpdateProductReviewUseCase:
    return container.resolve(UpdateProductReviewUseCase)
