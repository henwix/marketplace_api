from dataclasses import dataclass

from django.db import transaction

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.common.exceptions.commands import NothingToUpdateError
from src.apps.products.commands.product_reviews import UpdateProductReviewCommand
from src.apps.products.entities.product_reviews import ProductReviewEntity
from src.apps.products.services.product_reviews import BaseProductReviewService
from src.apps.products.services.products import BaseProductService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class UpdateProductReviewUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    product_review_service: BaseProductReviewService
    auth_validator_service: BaseAuthValidatorService

    def execute(self, command: UpdateProductReviewCommand) -> ProductReviewEntity:
        if command.is_empty:
            raise NothingToUpdateError
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        with transaction.atomic():
            product = self.product_service.try_get_for_update_by_id(id=command.product_id)
            product_review = self.product_review_service.try_get_by_user_id_and_product_id(
                user_id=user.id,
                product_id=product.id,
            )
            old_rating = product_review.rating
            product_review.update(rating=command.rating, text=command.text)
            product.apply_update_review_data(old_rating=old_rating, new_rating=product_review.rating)
            product_review = self.product_review_service.save(product_review=product_review, update=True)
            self.product_service.save(product=product, update=True)
        return product_review
