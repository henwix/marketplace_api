from src.apps.products.entities.product_reviews import ProductReviewEntity
from src.apps.products.models.product_reviews import ProductReview


def data_to_product_review_entity(data: dict) -> ProductReviewEntity:
    return ProductReviewEntity(**data)


def product_review_from_entity(entity: ProductReviewEntity) -> ProductReview:
    return ProductReview(
        pk=entity.id,
        user_id=entity.user_id,
        product_id=entity.product_id,
        rating=entity.rating,
        text=entity.text,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def product_review_to_entity(dto: ProductReview) -> ProductReviewEntity:
    return ProductReviewEntity(
        id=dto.pk,
        user_id=dto.user_id,
        product_id=dto.product_id,
        rating=dto.rating,
        text=dto.text,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
    )
