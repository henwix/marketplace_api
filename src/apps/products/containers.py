from punq import Container

from src.apps.products.repositories.product_variants import BaseProductVariantRepository, ORMProductVariantRepository
from src.apps.products.repositories.products import BaseProductRepository, ORMProductRepository
from src.apps.products.services.product_variants import (
    BaseProductVariantAccessValidatorService,
    BaseProductVariantService,
    ProductVariantAccessValidatorService,
    ProductVariantService,
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
    # use cases
    container.register(CreateProductUseCase)
    container.register(GetProductByIdUseCase)
    container.register(GetProductBySlugUseCase)
    container.register(GlobalSearchProductUseCase)
    container.register(PersonalSearchProductUseCase)
    container.register(UpdateProductUseCase)
    container.register(DeleteProductUseCase)

    container.register(CreateProductVariantUseCase)
    container.register(GetProductVariantsUseCase)
    container.register(UpdateProductVariantUseCase)
    container.register(DeleteProductVariantUseCase)

    # services
    container.register(BaseProductService, ProductService)
    container.register(BaseProductAccessValidatorService, ProductAccessValidatorService)
    container.register(BaseProductHasVariantsValidatorService, ProductHasVariantsValidatorService)
    container.register(BaseProductVariantsLimitValidatorService, ProductVariantsLimitValidatorService)
    container.register(BaseProductVariantService, ProductVariantService)
    container.register(BaseProductVariantAccessValidatorService, ProductVariantAccessValidatorService)

    # repositories
    container.register(BaseProductRepository, ORMProductRepository)
    container.register(BaseProductVariantRepository, ORMProductVariantRepository)
