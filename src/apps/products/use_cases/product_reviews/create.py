from dataclasses import dataclass

from django.db import transaction

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.commands.product_reviews import CreateProductReviewCommand
from src.apps.products.converters.product_reviews import data_to_product_review_entity
from src.apps.products.entities.product_reviews import ProductReviewEntity
from src.apps.products.services.product_reviews import BaseProductReviewService, BaseSingleProductReviewValidatorService
from src.apps.products.services.products import BaseProductService
from src.apps.users.services.users import BaseUserService


@dataclass
class CreateProductReviewUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    product_review_service: BaseProductReviewService
    auth_validator_service: BaseAuthValidatorService
    product_review_validator_service: BaseSingleProductReviewValidatorService

    def execute(self, command: CreateProductReviewCommand) -> ProductReviewEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id(id=command.user_id)
        with transaction.atomic():
            product = self.product_service.try_get_for_update_by_id(id=command.product_id)
            self.product_review_validator_service.validate(user=user, product=product)
            product_review = data_to_product_review_entity(
                data={**command.data, 'user_id': user.id, 'product_id': product.id}
            )
            product.apply_create_review_data(rating=product_review.rating)
            product_review = self.product_review_service.save(product_review=product_review, update=False)
            self.product_service.save(product=product, update=True)
        return product_review
