from abc import ABC, abstractmethod
from uuid import UUID

from src.apps.products.models.product_reviews import ProductReview


class BaseProductReviewRepository(ABC):
    @abstractmethod
    def check_review_exists(self, user_id: int, product_id: UUID) -> bool: ...

    @abstractmethod
    def save(self, review: ProductReview, update: bool) -> ProductReview: ...

    @abstractmethod
    def get_for_update_by_id(self, id: int) -> ProductReview | None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class ProductReviewRepository(BaseProductReviewRepository):
    def check_review_exists(self, user_id: int, product_id: UUID) -> bool:
        return ProductReview.objects.filter(user_id=user_id, product_id=product_id).exists()

    def save(self, review: ProductReview, update: bool) -> ProductReview:
        review.save(force_update=update)
        return review

    def get_for_update_by_id(self, id: int) -> ProductReview | None:
        return ProductReview.objects.select_for_update().filter(pk=id).first()

    def delete(self, id: int) -> None:
        ProductReview.objects.filter(pk=id).delete()
