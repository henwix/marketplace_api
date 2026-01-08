from decimal import ROUND_HALF_UP, Decimal

from src.apps.products.models.products import Product
from tests.v1.products.factories import ProductModelFactory, ProductVariantModelFactory


def create_test_products_with_variant(products_params: dict, variant_params: dict | None = None) -> None:
    products = ProductModelFactory.create_batch(**products_params)
    for product in products:
        if variant_params:
            ProductVariantModelFactory.create(product=product, **variant_params)
        else:
            ProductVariantModelFactory.create(product=product)


def calculate_final_avg_rating(ratings: list[int]) -> Decimal:
    reviews_count = 0
    reviews_avg_rating = Decimal('0')

    for rating in ratings:
        total = reviews_avg_rating * reviews_count
        reviews_count += 1
        reviews_avg_rating = ((total + Decimal(rating)) / reviews_count).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    return reviews_avg_rating


def calculate_expected_avg_and_count_after_review_delete(product: Product, rating: int) -> tuple[int, Decimal]:
    if product.reviews_count <= 1:
        return 0, Decimal('0')
    else:
        total = product.reviews_avg_rating * product.reviews_count
        new_count = product.reviews_count - 1
        new_avg = ((total - Decimal(rating)) / new_count).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return new_count, new_avg


def calculate_expected_avg_rating_after_review_update(
    product: Product,
    old_rating: int,
    new_rating: int,
) -> Decimal:
    total = product.reviews_avg_rating * product.reviews_count
    total = total - Decimal(old_rating) + Decimal(new_rating)
    return (total / product.reviews_count).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
