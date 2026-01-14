from uuid import uuid7

import pytest

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError
from src.apps.common.exceptions import NothingToUpdateError
from src.apps.products.commands.product_reviews import CreateProductReviewCommand, UpdateProductReviewCommand
from src.apps.products.converters.product_reviews import product_review_to_entity
from src.apps.products.entities.product_reviews import ProductReviewEntity
from src.apps.products.exceptions.product_reviews import ProductReviewNotFoundError
from src.apps.products.exceptions.products import ProductNotFoundByIdError
from src.apps.products.models.product_reviews import ProductReview
from src.apps.products.models.products import Product
from src.apps.products.use_cases.product_reviews.create import CreateProductReviewUseCase
from src.apps.products.use_cases.product_reviews.update import UpdateProductReviewUseCase
from src.apps.users.exceptions.users import UserNotActiveError, UserNotFoundError
from src.apps.users.models import User
from tests.v1.products.utils import calculate_expected_avg_rating_after_review_update
from tests.v1.users.factories import UserModelFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames='expected_new_rating, expected_new_text',
    argvalues=[
        (5, 'New Updated Review text'),
        (2, 'Updated Text'),
    ],
)
def test_update_review_updated_one(
    create_product_review_use_case: CreateProductReviewUseCase,
    update_product_review_use_case: UpdateProductReviewUseCase,
    user: User,
    product: Product,
    expected_new_rating: int,
    expected_new_text: str,
):
    create_command = CreateProductReviewCommand(user_id=user.pk, product_id=product.pk, rating=1, text='1')
    create_product_review_use_case.execute(command=create_command)

    update_command = UpdateProductReviewCommand(
        user_id=user.pk, product_id=product.pk, rating=expected_new_rating, text=expected_new_text
    )
    updated_review = update_product_review_use_case.execute(command=update_command)
    db_review = ProductReview.objects.get(pk=updated_review.id)
    product.refresh_from_db()

    assert isinstance(updated_review, ProductReviewEntity)
    assert updated_review == product_review_to_entity(dto=db_review)
    assert product.reviews_count == 1
    assert product.reviews_avg_rating == expected_new_rating
    assert updated_review.rating == expected_new_rating
    assert updated_review.text == expected_new_text


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames='expected_new_rating, expected_new_text',
    argvalues=[
        (5, 'New Updated Review text'),
        (2, 'Updated Text'),
    ],
)
def test_update_review_updated_one_partial(
    create_product_review_use_case: CreateProductReviewUseCase,
    update_product_review_use_case: UpdateProductReviewUseCase,
    user: User,
    product: Product,
    expected_new_rating: int,
    expected_new_text: str,
):
    create_command = CreateProductReviewCommand(user_id=user.pk, product_id=product.pk, rating=1, text='1')
    create_product_review_use_case.execute(command=create_command)

    update_command = UpdateProductReviewCommand(user_id=user.pk, product_id=product.pk, rating=expected_new_rating)
    updated_review = update_product_review_use_case.execute(command=update_command)
    db_review = ProductReview.objects.get(pk=updated_review.id)
    product.refresh_from_db()
    assert updated_review == product_review_to_entity(dto=db_review)
    assert product.reviews_count == 1
    assert product.reviews_avg_rating == expected_new_rating
    assert updated_review.rating == expected_new_rating

    update_command = UpdateProductReviewCommand(user_id=user.pk, product_id=product.pk, text=expected_new_text)
    updated_review = update_product_review_use_case.execute(command=update_command)
    db_review = ProductReview.objects.get(pk=updated_review.id)
    assert updated_review == product_review_to_entity(dto=db_review)
    assert updated_review.text == expected_new_text


@pytest.mark.django_db
@pytest.mark.parametrize(
    argnames='expected_old_ratings, expected_new_ratings',
    argvalues=(
        [[5, 3, 4], [4, 1, 2]],
        [[4, 4, 4, 1, 3, 3, 2], [5, 3, 2, 2, 5, 1, 5]],
        [[1, 5, 4, 4, 3, 3, 3, 1, 2, 3, 3, 1], [4, 4, 5, 2, 1, 3, 4, 1, 1, 5, 3, 2]],
        [[3, 1, 5, 2, 4, 1, 3, 5, 2, 2, 4, 1, 5, 3, 2], [3, 5, 4, 2, 2, 2, 2, 3, 2, 1, 4, 1, 3, 1, 2]],
        [[4, 1, 3, 5, 2, 1, 4, 1, 2, 3, 2, 1, 5, 4, 3, 2, 5], [5, 2, 1, 4, 2, 5, 2, 4, 1, 5, 5, 2, 4, 1, 2, 4, 1]],
    ),
)
def test_update_review_updated_many(
    create_product_review_use_case: CreateProductReviewUseCase,
    update_product_review_use_case: UpdateProductReviewUseCase,
    product: Product,
    expected_old_ratings: list[int],
    expected_new_ratings: list[int],
):
    users = UserModelFactory.create_batch(size=len(expected_old_ratings))
    for user, rating in zip(users, expected_old_ratings, strict=True):
        create_command = CreateProductReviewCommand(user_id=user.pk, product_id=product.pk, rating=rating, text='test')
        create_product_review_use_case.execute(command=create_command)
    product.refresh_from_db()

    for user, old_rating, new_rating in zip(users, expected_old_ratings, expected_new_ratings, strict=True):
        expected_reviews_avg_rating = calculate_expected_avg_rating_after_review_update(
            product=product, old_rating=old_rating, new_rating=new_rating
        )

        update_command = UpdateProductReviewCommand(user_id=user.pk, product_id=product.pk, rating=new_rating)
        update_product_review_use_case.execute(command=update_command)
        product.refresh_from_db()
        assert product.reviews_count == len(expected_old_ratings)
        assert product.reviews_avg_rating == expected_reviews_avg_rating


def test_update_review_not_updated_and_nothing_to_update_error_raised(
    update_product_review_use_case: UpdateProductReviewUseCase,
):
    command = UpdateProductReviewCommand(user_id=None, product_id=uuid7())
    with pytest.raises(NothingToUpdateError):
        update_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_review_not_updated_and_product_not_found_error_raised(
    update_product_review_use_case: UpdateProductReviewUseCase,
    user: User,
):
    with pytest.raises(ProductNotFoundByIdError):
        command = UpdateProductReviewCommand(user_id=user.pk, product_id=uuid7(), rating=1)
        update_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_review_not_updated_and_product_review_not_found_error_raised(
    update_product_review_use_case: UpdateProductReviewUseCase,
    user: User,
    product: Product,
):
    with pytest.raises(ProductReviewNotFoundError):
        command = UpdateProductReviewCommand(user_id=user.pk, product_id=product.pk, rating=1)
        update_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_review_user_credentials_error_raised(update_product_review_use_case: UpdateProductReviewUseCase):
    with pytest.raises(AuthCredentialsNotProvidedError):
        command = UpdateProductReviewCommand(user_id=None, product_id=uuid7(), rating=1)
        update_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_review_user_not_found_error_raised(update_product_review_use_case: UpdateProductReviewUseCase):
    with pytest.raises(UserNotFoundError):
        command = UpdateProductReviewCommand(user_id=1, product_id=uuid7(), rating=1)
        update_product_review_use_case.execute(command=command)


@pytest.mark.django_db
def test_update_review_user_not_active_error_raised(update_product_review_use_case: UpdateProductReviewUseCase):
    user = UserModelFactory.create(is_active=False)
    with pytest.raises(UserNotActiveError):
        command = UpdateProductReviewCommand(user_id=user.pk, product_id=uuid7(), rating=1)
        update_product_review_use_case.execute(command=command)
