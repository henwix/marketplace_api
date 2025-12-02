import punq

from src.apps.products.repositories.products import BaseProductRepository, ORMProductRepository
from src.apps.products.services.products import BaseProductService, ProductService
from src.apps.products.use_cases.create_product import CreateProductUseCase


def init_products(container: punq.Container) -> None:
    # use cases
    container.register(CreateProductUseCase)

    # services
    container.register(BaseProductService, ProductService)

    # repositories
    container.register(BaseProductRepository, ORMProductRepository)
