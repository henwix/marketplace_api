from collections.abc import Iterable
from dataclasses import dataclass

from src.apps.products.commands.product_reviews import GetProductReviewsCommand
from src.apps.products.models.product_reviews import ProductReview
from src.apps.products.services.product_reviews import BaseProductReviewService
from src.apps.products.services.products import BaseProductService


@dataclass(eq=False)
class GetProductReviewsUseCase:
    product_service: BaseProductService
    product_review_service: BaseProductReviewService

    def execute(self, command: GetProductReviewsCommand) -> Iterable[ProductReview]:
        product = self.product_service.try_get_by_id(id=command.product_id)
        reviews = self.product_review_service.get_many_by_product_id_with_loaded_user(product_id=product.id)
        return reviews
