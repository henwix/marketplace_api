from uuid import uuid7

import pytest

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.products.commands.product_reviews import CreateProductReviewCommand
from src.apps.products.converters.product_reviews import product_review_to_entity
from src.apps.products.entities.product_reviews import ProductReviewEntity
from src.apps.products.exceptions.product_reviews import ProductReviewAlreadyExistsError
from src.apps.products.exceptions.products import ProductNotFoundByIdError
from src.apps.products.models.product_reviews import ProductReview
from src.apps.products.models.products import Product
from src.apps.products.use_cases.product_reviews.create import CreateProductReviewUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.products.factories import ProductReviewModelFactory
from tests.v1.products.test_data.product_reviews_data import (
    PRODUCT_REVIEWS_RATINGS_ARGNAMES,
    PRODUCT_REVIEWS_RATINGS_ARGVALUES,
)
from tests.v1.products.utils import calculate_final_avg_rating
from tests.v1.users.factories import UserModelFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames='expected_rating, expected_text',
    argvalues=[
        [1, 'test_text'],
        [2, 'Text Review'],
        [3, 'textreview'],
        [4, 'TeSt Text ReVieW'],
        [5, 'asfhkjashag'],
    ],
)
def test_create_review_created_one(
    create_product_review_use_case: CreateProductReviewUseCase,
    product: Product,
    user: User,
    expected_rating: int,
    expected_text: str,
):
    command = CreateProductReviewCommand(
        user_id=user.pk, product_id=product.pk, rating=expected_rating, text=expected_text
    )
    review = create_product_review_use_case.execute(command=command)
    db_review = ProductReview.objects.get(user_id=user.pk, product_id=product.pk, rating=expected_rating)
    db_product = Product.objects.get(pk=product.pk)

    assert isinstance(review, ProductReviewEntity)
    assert review == product_review_to_entity(dto=db_review)
    assert db_product.reviews_count == 1
    assert db_product.reviews_avg_rating == expected_rating


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_REVIEWS_RATINGS_ARGNAMES, argvalues=PRODUCT_REVIEWS_RATINGS_ARGVALUES)
def test_create_review_created_many(
    create_product_review_use_case: CreateProductReviewUseCase,
    product: Product,
    expected_ratings: list[int],
):
    expected_reviews_count = len(expected_ratings)
    expected_reviews_avg_rating = calculate_final_avg_rating(ratings=expected_ratings)
    users = UserModelFactory.create_batch(size=expected_reviews_count)
    for user, rating in zip(users, expected_ratings, strict=True):
        command = CreateProductReviewCommand(user_id=user.pk, product_id=product.pk, rating=rating, text='text')
        create_product_review_use_case.execute(command=command)

    db_product = Product.objects.get(pk=product.pk)
    assert db_product.reviews_count == expected_reviews_count
    assert db_product.reviews_avg_rating == expected_reviews_avg_rating


@pytest.mark.django_db
def test_create_review_not_created_and_product_not_found_error_raised(
    create_product_review_use_case: CreateProductReviewUseCase,
    user: User,
):
    with pytest.raises(ProductNotFoundByIdError):
        command = CreateProductReviewCommand(user_id=user.pk, product_id=uuid7(), rating=1, text='1')
        create_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_create_review_not_created_and_review_already_exists_error_raised(
    create_product_review_use_case: CreateProductReviewUseCase,
    user: User,
    product: Product,
):
    ProductReviewModelFactory.create(user=user, product=product)
    with pytest.raises(ProductReviewAlreadyExistsError):
        command = CreateProductReviewCommand(user_id=user.pk, product_id=product.pk, rating=1, text='1')
        create_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_create_review_user_credentials_error_raised(create_product_review_use_case: CreateProductReviewUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        command = CreateProductReviewCommand(user_id=None, product_id=uuid7(), rating=1, text='1')
        create_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_create_review_user_not_found_error_raised(create_product_review_use_case: CreateProductReviewUseCase):
    with pytest.raises(UserNotFoundError):
        command = CreateProductReviewCommand(user_id=1, product_id=uuid7(), rating=1, text='1')
        create_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_create_review_user_not_active_error_raised(create_product_review_use_case: CreateProductReviewUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        command = CreateProductReviewCommand(user_id=user.pk, product_id=uuid7(), rating=1, text='1')
        create_product_review_use_case.execute(command=command)
