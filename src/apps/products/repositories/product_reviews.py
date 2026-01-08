from abc import ABC, abstractmethod
from collections.abc import Iterable
from uuid import UUID

from src.apps.products.models.product_reviews import ProductReview


class BaseProductReviewRepository(ABC):
    @abstractmethod
    def check_review_exists(self, user_id: int, product_id: UUID) -> bool: ...

    @abstractmethod
    def save(self, review: ProductReview, update: bool) -> ProductReview: ...

    @abstractmethod
    def get_by_user_id_and_product_id(self, user_id: int, product_id: UUID) -> ProductReview | None: ...

    @abstractmethod
    def get_many_by_product_id_with_loaded_user(self, product_id: UUID) -> Iterable[ProductReview]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class ORMProductReviewRepository(BaseProductReviewRepository):
    def check_review_exists(self, user_id: int, product_id: UUID) -> bool:
        return ProductReview.objects.filter(user_id=user_id, product_id=product_id).exists()

    def save(self, review: ProductReview, update: bool) -> ProductReview:
        review.save(force_update=update)
        return review

    def get_by_user_id_and_product_id(self, user_id: int, product_id: UUID) -> ProductReview | None:
        return ProductReview.objects.filter(user_id=user_id, product_id=product_id).first()

    def get_many_by_product_id_with_loaded_user(self, product_id: UUID) -> Iterable[ProductReview]:
        return ProductReview.objects.select_related('user').filter(product_id=product_id)

    def delete(self, id: int) -> None:
        ProductReview.objects.filter(pk=id).delete()
