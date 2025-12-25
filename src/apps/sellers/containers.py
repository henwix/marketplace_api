from punq import Container

from src.apps.sellers.repositories.sellers import BaseSellerRepository, ORMSellerRepository
from src.apps.sellers.services.sellers import (
    BaseSellerAlreadyExistsValidatorService,
    BaseSellerDoesNotExistValidatorService,
    BaseSellerService,
    SellerAlreadyExistsValidatorService,
    SellerDoesNotExistValidatorService,
    SellerService,
)
from src.apps.sellers.use_cases.create import CreateSellerUseCase
from src.apps.sellers.use_cases.delete import DeleteSellerUseCase
from src.apps.sellers.use_cases.get import GetSellerUseCase
from src.apps.sellers.use_cases.get_by_id import GetSellerByIdUseCase
from src.apps.sellers.use_cases.update import UpdateSellerUseCase


def init_sellers(container: Container) -> None:
    # use cases
    container.register(CreateSellerUseCase)
    container.register(GetSellerUseCase)
    container.register(GetSellerByIdUseCase)
    container.register(UpdateSellerUseCase)
    container.register(DeleteSellerUseCase)

    # services
    container.register(BaseSellerService, SellerService)
    container.register(BaseSellerAlreadyExistsValidatorService, SellerAlreadyExistsValidatorService)
    container.register(BaseSellerDoesNotExistValidatorService, SellerDoesNotExistValidatorService)

    # repositories
    container.register(BaseSellerRepository, ORMSellerRepository)
