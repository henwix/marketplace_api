from uuid import uuid7

import pytest

from src.apps.products.commands.product_reviews import CreateProductReviewCommand, GetProductReviewsCommand
from src.apps.products.exceptions.products import ProductNotFoundByIdError
from src.apps.products.models.product_reviews import ProductReview
from src.apps.products.models.products import Product
from src.apps.products.use_cases.product_reviews.create import CreateProductReviewUseCase
from src.apps.products.use_cases.product_reviews.get import GetProductReviewsUseCase
from tests.v1.products.test_data.product_reviews_data import (
    PRODUCT_REVIEWS_RATINGS_ARGNAMES,
    PRODUCT_REVIEWS_RATINGS_ARGVALUES,
)
from tests.v1.users.factories import UserModelFactory


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_REVIEWS_RATINGS_ARGNAMES, argvalues=PRODUCT_REVIEWS_RATINGS_ARGVALUES)
def test_get_product_reviews_retrieved(
    create_product_review_use_case: CreateProductReviewUseCase,
    get_product_reviews_use_case: GetProductReviewsUseCase,
    product: Product,
    expected_ratings: list[int],
):
    expected_reviews_count = len(expected_ratings)
    users = UserModelFactory.create_batch(size=expected_reviews_count)
    for user, rating in zip(users, expected_ratings, strict=True):
        create_command = CreateProductReviewCommand(
            user_id=user.pk, product_id=product.pk, data={'rating': rating, 'text': 'test'}
        )
        create_product_review_use_case.execute(command=create_command)

    get_command = GetProductReviewsCommand(product_id=product.pk)
    reviews = get_product_reviews_use_case.execute(command=get_command)

    assert len(reviews) == expected_reviews_count
    for review, expected_user, expected_rating in zip(reviews, users, expected_ratings, strict=True):
        assert isinstance(review, ProductReview)
        assert review.rating == expected_rating
        assert review._state.fields_cache.get('user') == expected_user


@pytest.mark.django_db
def test_get_product_reviews_retrieved_with_zero_reviews(
    get_product_reviews_use_case: GetProductReviewsUseCase,
    product: Product,
):
    get_command = GetProductReviewsCommand(product_id=product.pk)
    reviews = get_product_reviews_use_case.execute(command=get_command)
    assert len(reviews) == 0


@pytest.mark.django_db
def test_get_product_reviews_not_retrieved_and_product_not_found_error_raised(
    get_product_reviews_use_case: GetProductReviewsUseCase,
):
    with pytest.raises(ProductNotFoundByIdError):
        command = GetProductReviewsCommand(product_id=uuid7())
        get_product_reviews_use_case.execute(command=command)
