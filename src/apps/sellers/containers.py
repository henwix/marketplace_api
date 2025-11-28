import punq

from src.apps.sellers.repositories.sellers import BaseSellerRepository, ORMSellerRepository
from src.apps.sellers.services.sellers import BaseSellerService, SellerService
from src.apps.sellers.use_cases.create import CreateSellerUseCase


def init_sellers(container: punq.Container) -> None:
    # use cases
    container.register(CreateSellerUseCase)

    # services
    container.register(BaseSellerService, SellerService)

    # repositories
    container.register(BaseSellerRepository, ORMSellerRepository)
