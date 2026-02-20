from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from src.apps.products.entities.product_reviews import ProductReviewEntity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.product_reviews import (
    ProductReviewAlreadyExistsError,
    ProductReviewNotFoundError,
)
from src.apps.products.models.product_reviews import ProductReview
from src.apps.products.repositories.product_reviews import BaseProductReviewRepository
from src.apps.users.entities import UserEntity


class BaseSingleProductReviewValidatorService(ABC):
    @abstractmethod
    def validate(self, user: UserEntity, product: ProductEntity) -> None: ...


@dataclass(eq=False)
class SingleProductReviewValidatorService(BaseSingleProductReviewValidatorService):
    product_review_service: BaseProductReviewService

    def validate(self, user: UserEntity, product: ProductEntity) -> None:
        if self.product_review_service.check_review_exists(user_id=user.id, product_id=product.id):
            raise ProductReviewAlreadyExistsError(user_id=user.id, product_id=product.id)


class BaseProductReviewService(ABC):
    @abstractmethod
    def check_review_exists(self, user_id: int, product_id: UUID) -> bool: ...

    @abstractmethod
    def save(self, product_review: ProductReviewEntity, update: bool = False) -> ProductReviewEntity: ...

    @abstractmethod
    def try_get_by_user_id_and_product_id(self, user_id: int, product_id: UUID) -> ProductReviewEntity: ...

    @abstractmethod
    def get_many_by_product_id_with_loaded_user(self, product_id: UUID) -> Iterable[ProductReview]: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


@dataclass(eq=False)
class ProductReviewService(BaseProductReviewService):
    repository: BaseProductReviewRepository

    def check_review_exists(self, user_id: int, product_id: UUID) -> bool:
        return self.repository.check_review_exists(user_id=user_id, product_id=product_id)

    def save(self, product_review: ProductReviewEntity, update: bool = False) -> ProductReviewEntity:
        return self.repository.save(review=product_review, update=update)

    def try_get_by_user_id_and_product_id(self, user_id: int, product_id: UUID) -> ProductReviewEntity:
        review = self.repository.get_by_user_id_and_product_id(user_id=user_id, product_id=product_id)
        if review is None:
            raise ProductReviewNotFoundError(user_id=user_id, product_id=product_id)
        return review

    def get_many_by_product_id_with_loaded_user(self, product_id: UUID) -> Iterable[ProductReview]:
        return self.repository.get_many_by_product_id_with_loaded_user(product_id=product_id)

    def delete(self, id: int) -> None:
        self.repository.delete(id=id)
