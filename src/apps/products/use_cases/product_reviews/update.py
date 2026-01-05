from dataclasses import dataclass

from django.db import transaction

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.commands.product_reviews import UpdateProductReviewCommand
from src.apps.products.entities.product_reviews import ProductReviewEntity
from src.apps.products.services.product_reviews import BaseProductReviewAccessValidatorService, BaseProductReviewService
from src.apps.products.services.products import BaseProductService
from src.apps.users.services.users import BaseUserService


@dataclass
class UpdateProductReviewUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    product_review_service: BaseProductReviewService
    auth_validator_service: BaseAuthValidatorService
    review_access_validator_service: BaseProductReviewAccessValidatorService

    def execute(self, command: UpdateProductReviewCommand) -> ProductReviewEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id(id=command.user_id)
        with transaction.atomic():
            product_review = self.product_review_service.try_get_for_update_by_id(id=command.product_review_id)
            self.review_access_validator_service.validate(user=user, product_review=product_review)
            old_rating = product_review.rating
            product_review.update_from_data(data=command.data)
            product = self.product_service.try_get_for_update_by_id(id=product_review.product_id)
            product.apply_update_review_data(old_rating=old_rating, new_rating=product_review.rating)
            product_review = self.product_review_service.save(product_review=product_review, update=True)
            self.product_service.save(product=product, update=True)
        return product_review
