from punq import Container

from src.apps.products.repositories.product_reviews import BaseProductReviewRepository, ORMProductReviewRepository
from src.apps.products.repositories.product_variants import BaseProductVariantRepository, ORMProductVariantRepository
from src.apps.products.repositories.products import BaseProductRepository, ORMProductRepository
from src.apps.products.services.product_reviews import (
    BaseProductReviewService,
    BaseSingleProductReviewValidatorService,
    ProductReviewService,
    SingleProductReviewValidatorService,
)
from src.apps.products.services.product_variants import (
    BaseProductVariantAccessValidatorService,
    BaseProductVariantService,
    BaseProductVariantStockValidatorService,
    BaseProductVariantVisibilityValidatorService,
    ComposedProductVariantStockValidatorService,
    ProductVariantAccessValidatorService,
    ProductVariantAvailableQuantityValidatorService,
    ProductVariantPositiveStockValidatorService,
    ProductVariantService,
    ProductVariantVisibilityValidatorService,
)
from src.apps.products.services.products import (
    BaseProductAccessValidatorService,
    BaseProductHasVariantsValidatorService,
    BaseProductService,
    BaseProductVariantsLimitValidatorService,
    ProductAccessValidatorService,
    ProductHasVariantsValidatorService,
    ProductService,
    ProductVariantsLimitValidatorService,
)
from src.apps.products.use_cases.product_reviews.create import CreateProductReviewUseCase
from src.apps.products.use_cases.product_reviews.delete import DeleteProductReviewUseCase
from src.apps.products.use_cases.product_reviews.get import GetProductReviewsUseCase
from src.apps.products.use_cases.product_reviews.update import UpdateProductReviewUseCase
from src.apps.products.use_cases.product_variants.create import CreateProductVariantUseCase
from src.apps.products.use_cases.product_variants.delete import DeleteProductVariantUseCase
from src.apps.products.use_cases.product_variants.get import GetProductVariantsUseCase
from src.apps.products.use_cases.product_variants.update import UpdateProductVariantUseCase
from src.apps.products.use_cases.products.create import CreateProductUseCase
from src.apps.products.use_cases.products.delete import DeleteProductUseCase
from src.apps.products.use_cases.products.get_by_id import GetProductByIdUseCase
from src.apps.products.use_cases.products.get_by_slug import GetProductBySlugUseCase
from src.apps.products.use_cases.products.global_search import GlobalSearchProductUseCase
from src.apps.products.use_cases.products.personal_search import PersonalSearchProductUseCase
from src.apps.products.use_cases.products.update import UpdateProductUseCase


def init_products(container: Container) -> None:
    def _build_product_variant_stock_validator() -> BaseProductVariantStockValidatorService:
        return ComposedProductVariantStockValidatorService(
            validators=[
                container.resolve(ProductVariantPositiveStockValidatorService),
                container.resolve(ProductVariantAvailableQuantityValidatorService),
            ]
        )

    # Products use cases
    container.register(CreateProductUseCase)
    container.register(GetProductByIdUseCase)
    container.register(GetProductBySlugUseCase)
    container.register(GlobalSearchProductUseCase)
    container.register(PersonalSearchProductUseCase)
    container.register(UpdateProductUseCase)
    container.register(DeleteProductUseCase)

    # Product Variants use cases
    container.register(CreateProductVariantUseCase)
    container.register(GetProductVariantsUseCase)
    container.register(UpdateProductVariantUseCase)
    container.register(DeleteProductVariantUseCase)

    # Product Reviews use cases
    container.register(CreateProductReviewUseCase)
    container.register(GetProductReviewsUseCase)
    container.register(DeleteProductReviewUseCase)
    container.register(UpdateProductReviewUseCase)

    # Products services
    container.register(BaseProductService, ProductService)
    container.register(BaseProductAccessValidatorService, ProductAccessValidatorService)
    container.register(BaseProductHasVariantsValidatorService, ProductHasVariantsValidatorService)
    container.register(BaseProductVariantsLimitValidatorService, ProductVariantsLimitValidatorService)

    # Product Variants services
    container.register(BaseProductVariantService, ProductVariantService)
    container.register(BaseProductVariantAccessValidatorService, ProductVariantAccessValidatorService)
    container.register(BaseProductVariantVisibilityValidatorService, ProductVariantVisibilityValidatorService)
    container.register(ProductVariantPositiveStockValidatorService)
    container.register(ProductVariantAvailableQuantityValidatorService)
    container.register(
        BaseProductVariantStockValidatorService,
        factory=_build_product_variant_stock_validator,
    )

    # Product Reviews services
    container.register(BaseProductReviewService, ProductReviewService)
    container.register(BaseSingleProductReviewValidatorService, SingleProductReviewValidatorService)

    # repositories
    container.register(BaseProductRepository, ORMProductRepository)

    container.register(BaseProductVariantRepository, ORMProductVariantRepository)

    container.register(BaseProductReviewRepository, ORMProductReviewRepository)
