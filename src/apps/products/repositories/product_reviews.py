from abc import ABC, abstractmethod
from collections.abc import Iterable
from uuid import UUID

from src.apps.products.converters.product_reviews import product_review_from_entity, product_review_to_entity
from src.apps.products.entities.product_reviews import ProductReviewEntity
from src.apps.products.models.product_reviews import ProductReview


class BaseProductReviewRepository(ABC):
    @abstractmethod
    def check_review_exists(self, user_id: int, product_id: UUID) -> bool: ...

    @abstractmethod
    def save(self, review: ProductReviewEntity, update: bool) -> ProductReviewEntity: ...

    @abstractmethod
    def get_by_user_id_and_product_id(self, user_id: int, product_id: UUID) -> ProductReviewEntity | None: ...

    @abstractmethod
    def get_many_by_product_id_with_loaded_user(self, product_id: UUID) -> Iterable[ProductReview]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class ORMProductReviewRepository(BaseProductReviewRepository):
    def check_review_exists(self, user_id: int, product_id: UUID) -> bool:
        return ProductReview.objects.filter(user_id=user_id, product_id=product_id).exists()

    def save(self, review: ProductReviewEntity, update: bool) -> ProductReviewEntity:
        dto = product_review_from_entity(entity=review)
        dto.save(force_update=update)
        return product_review_to_entity(dto=dto)

    def get_by_user_id_and_product_id(self, user_id: int, product_id: UUID) -> ProductReviewEntity | None:
        dto = ProductReview.objects.filter(user_id=user_id, product_id=product_id).first()
        return product_review_to_entity(dto=dto) if dto else None

    def get_many_by_product_id_with_loaded_user(self, product_id: UUID) -> Iterable[ProductReview]:
        return ProductReview.objects.select_related('user').filter(product_id=product_id)

    def delete(self, id: int) -> None:
        ProductReview.objects.filter(pk=id).delete()
