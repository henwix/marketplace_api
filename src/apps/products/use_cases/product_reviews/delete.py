from dataclasses import dataclass

from django.db import transaction

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.commands.product_reviews import DeleteProductReviewCommand
from src.apps.products.services.product_reviews import BaseProductReviewService
from src.apps.products.services.products import BaseProductService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class DeleteProductReviewUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    product_review_service: BaseProductReviewService
    auth_validator_service: BaseAuthValidatorService

    def execute(self, command: DeleteProductReviewCommand) -> None:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        with transaction.atomic():
            product = self.product_service.try_get_for_update_by_id(id=command.product_id)
            product_review = self.product_review_service.try_get_by_user_id_and_product_id(
                user_id=user.id,
                product_id=product.id,
            )
            product.apply_delete_review_data(rating=product_review.rating)
            self.product_review_service.delete(id=product_review.id)
            self.product_service.save(product=product, update=True)
