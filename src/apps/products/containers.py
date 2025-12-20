from punq import Container

from src.apps.products.repositories.product_variants import BaseProductVariantRepository, ORMProductVariantRepository
from src.apps.products.repositories.products import BaseProductRepository, ORMProductRepository
from src.apps.products.services.product_variants import (
    BaseProductVariantAuthorValidatorService,
    BaseProductVariantLimitValidatorService,
    BaseProductVariantService,
    BaseProductVariantsQuantityValidatorService,
    ProductVariantAuthorValidatorService,
    ProductVariantLimitValidatorService,
    ProductVariantService,
    ProductVariantsQuantityValidatorService,
)
from src.apps.products.services.products import (
    BaseProductAuthorValidatorService,
    BaseProductService,
    ProductAuthorValidatorService,
    ProductService,
)
from src.apps.products.use_cases.product_variants.create import CreateProductVariantUseCase
from src.apps.products.use_cases.product_variants.delete import DeleteProductVariantUseCase
from src.apps.products.use_cases.product_variants.get import GetProductVariantsUseCase
from src.apps.products.use_cases.product_variants.update import UpdateProductVariantUseCase
from src.apps.products.use_cases.products.create import CreateProductUseCase
from src.apps.products.use_cases.products.delete import DeleteProductUseCase
from src.apps.products.use_cases.products.get_by_id import GetProductByIdUseCase
from src.apps.products.use_cases.products.get_by_slug import GetProductBySlugUseCase
from src.apps.products.use_cases.products.update import UpdateProductUseCase


def init_products(container: Container) -> None:
    # use cases
    container.register(CreateProductUseCase)
    container.register(GetProductByIdUseCase)
    container.register(GetProductBySlugUseCase)
    container.register(UpdateProductUseCase)
    container.register(DeleteProductUseCase)

    container.register(CreateProductVariantUseCase)
    container.register(GetProductVariantsUseCase)
    container.register(UpdateProductVariantUseCase)
    container.register(DeleteProductVariantUseCase)

    # services
    container.register(BaseProductService, ProductService)
    container.register(BaseProductVariantService, ProductVariantService)
    container.register(BaseProductVariantLimitValidatorService, ProductVariantLimitValidatorService)
    container.register(BaseProductAuthorValidatorService, ProductAuthorValidatorService)

    container.register(BaseProductVariantAuthorValidatorService, ProductVariantAuthorValidatorService)
    container.register(BaseProductVariantsQuantityValidatorService, ProductVariantsQuantityValidatorService)

    # repositories
    container.register(BaseProductRepository, ORMProductRepository)
    container.register(BaseProductVariantRepository, ORMProductVariantRepository)
