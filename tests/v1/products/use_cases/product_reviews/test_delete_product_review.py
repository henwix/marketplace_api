from uuid import uuid7

import pytest

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.products.commands.product_reviews import CreateProductReviewCommand, DeleteProductReviewCommand
from src.apps.products.commands.product_variants import CreateProductVariantCommand
from src.apps.products.exceptions.product_reviews import ProductReviewNotFoundError
from src.apps.products.exceptions.products import ProductNotFoundByIdError
from src.apps.products.models.product_reviews import ProductReview
from src.apps.products.models.products import Product
from src.apps.products.use_cases.product_reviews.create import CreateProductReviewUseCase
from src.apps.products.use_cases.product_reviews.delete import DeleteProductReviewUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.products.test_data.product_reviews_data import (
    PRODUCT_REVIEWS_RATINGS_ARGNAMES,
    PRODUCT_REVIEWS_RATINGS_ARGVALUES,
)
from tests.v1.products.utils import calculate_expected_avg_and_count_after_review_delete
from tests.v1.users.factories import UserModelFactory


@pytest.mark.django_db
@pytest.mark.parametrize('expected_rating', [1, 2, 3, 4, 5])
def test_delete_review_deleted_one(
    create_product_review_use_case: CreateProductReviewUseCase,
    delete_product_review_use_case: DeleteProductReviewUseCase,
    user: User,
    product: Product,
    expected_rating: int,
):
    create_command = CreateProductVariantCommand(
        user_id=user.pk, product_id=product.pk, data={'rating': expected_rating, 'text': 'test'}
    )
    created_review = create_product_review_use_case.execute(command=create_command)
    db_product: Product = Product.objects.get(pk=product.pk)
    assert db_product.reviews_count == 1
    assert db_product.reviews_avg_rating == expected_rating
    assert ProductReview.objects.filter(pk=created_review.id).exists()

    delete_command = DeleteProductReviewCommand(user_id=user.pk, product_id=product.pk)
    delete_product_review_use_case.execute(command=delete_command)
    db_product: Product = Product.objects.get(pk=product.pk)
    assert db_product.reviews_count == 0
    assert db_product.reviews_avg_rating == 0
    assert not ProductReview.objects.filter(pk=created_review.id).exists()


@pytest.mark.django_db
@pytest.mark.parametrize(argnames=PRODUCT_REVIEWS_RATINGS_ARGNAMES, argvalues=PRODUCT_REVIEWS_RATINGS_ARGVALUES)
def test_delete_review_deleted_many(
    create_product_review_use_case: CreateProductReviewUseCase,
    delete_product_review_use_case: DeleteProductReviewUseCase,
    product: Product,
    expected_ratings: list[int],
):
    users = UserModelFactory.create_batch(size=len(expected_ratings))
    for user, rating in zip(users, expected_ratings, strict=True):
        create_command = CreateProductReviewCommand(
            user_id=user.pk, product_id=product.pk, data={'rating': rating, 'text': 'test'}
        )
        create_product_review_use_case.execute(command=create_command)
    product.refresh_from_db()

    for user, rating in zip(users, expected_ratings, strict=True):
        expected_reviews_count, expected_reviews_avg_rating = calculate_expected_avg_and_count_after_review_delete(
            product=product, rating=rating
        )

        delete_command = DeleteProductReviewCommand(user_id=user.pk, product_id=product.pk)
        delete_product_review_use_case.execute(command=delete_command)
        product.refresh_from_db()
        assert product.reviews_count == expected_reviews_count
        assert product.reviews_avg_rating == expected_reviews_avg_rating


@pytest.mark.django_db
def test_delete_review_not_deleted_and_product_not_found_error_raised(
    delete_product_review_use_case: DeleteProductReviewUseCase,
    user: User,
):
    with pytest.raises(ProductNotFoundByIdError):
        command = DeleteProductReviewCommand(user_id=user.id, product_id=uuid7())
        delete_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_review_not_deleted_and_product_review_not_found_error_raised(
    delete_product_review_use_case: DeleteProductReviewUseCase,
    user: User,
    product: Product,
):
    with pytest.raises(ProductReviewNotFoundError):
        command = DeleteProductReviewCommand(user_id=user.pk, product_id=product.pk)
        delete_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_review_user_credentials_error_raised(delete_product_review_use_case: DeleteProductReviewUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        command = DeleteProductReviewCommand(user_id=None, product_id=uuid7())
        delete_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_review_user_not_found_error_raised(delete_product_review_use_case: DeleteProductReviewUseCase):
    with pytest.raises(UserNotFoundError):
        command = DeleteProductReviewCommand(user_id=1, product_id=uuid7())
        delete_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_delete_review_user_not_active_error_raised(delete_product_review_use_case: DeleteProductReviewUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        command = DeleteProductReviewCommand(user_id=user.pk, product_id=uuid7())
        delete_product_review_use_case.execute(command=command)
