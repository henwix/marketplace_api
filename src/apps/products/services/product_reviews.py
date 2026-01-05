from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.products.converters.product_reviews import product_review_from_entity, product_review_to_entity
from src.apps.products.entities.product_reviews import ProductReviewEntity
from src.apps.products.entities.products import ProductEntity
from src.apps.products.exceptions.product_reviews import (
    ProductReviewAccessForbiddenError,
    ProductReviewAlreadyExistsError,
    ProductReviewNotFoundError,
)
from src.apps.products.repositories.product_reviews import BaseProductReviewRepository
from src.apps.users.entities import UserEntity


class BaseSingleProductReviewValidatorService(ABC):
    @abstractmethod
    def validate(self, user: UserEntity, product: ProductEntity) -> None: ...


@dataclass
class SingleProductReviewValidatorService(BaseSingleProductReviewValidatorService):
    product_review_service: BaseProductReviewService

    def validate(self, user: UserEntity, product: ProductEntity) -> None:
        if self.product_review_service.check_review_exists(user=user, product=product):
            raise ProductReviewAlreadyExistsError(user_id=user.id, product_id=product.id)


class BaseProductReviewAccessValidatorService(ABC):
    @abstractmethod
    def validate(self, user: UserEntity, product_review: ProductReviewEntity) -> None: ...


class ProductReviewAccessValidatorService(BaseProductReviewAccessValidatorService):
    def validate(self, user: UserEntity, product_review: ProductReviewEntity) -> None:
        if user.id != product_review.user_id:
            raise ProductReviewAccessForbiddenError(user_id=user.id, product_review_id=product_review.id)


class BaseProductReviewService(ABC):
    @abstractmethod
    def check_review_exists(self, user: UserEntity, product: ProductEntity) -> bool: ...

    @abstractmethod
    def save(self, product_review: ProductReviewEntity, update: bool = False) -> ProductReviewEntity: ...

    @abstractmethod
    def try_get_for_update_by_id(self, id: int) -> ProductReviewEntity: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


@dataclass
class ProductReviewService(BaseProductReviewService):
    repository: BaseProductReviewRepository

    def check_review_exists(self, user: UserEntity, product: ProductEntity) -> bool:
        return self.repository.check_review_exists(user_id=user.id, product_id=product.id)

    def save(self, product_review: ProductReviewEntity, update: bool = False) -> ProductReviewEntity:
        dto = product_review_from_entity(entity=product_review)
        dto = self.repository.save(review=dto, update=update)
        return product_review_to_entity(dto=dto)

    def try_get_for_update_by_id(self, id: int) -> ProductReviewEntity:
        dto = self.repository.get_for_update_by_id(id=id)
        if dto is None:
            raise ProductReviewNotFoundError(product_review_id=id)
        return product_review_to_entity(dto=dto)

    def delete(self, id: int) -> None:
        self.repository.delete(id=id)
