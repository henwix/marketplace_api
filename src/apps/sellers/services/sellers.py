from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.sellers.converters.sellers import seller_from_entity, seller_to_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.exceptions import SellerAlreadyExistsError, SellerNotFoundByIdError, SellerNotFoundError
from src.apps.sellers.repositories.sellers import BaseSellerRepository


class BaseSellerMustNotExistValidatorService(ABC):
    @abstractmethod
    def validate(self, seller: SellerEntity | None, user_id: int) -> None: ...


class SellerMustNotExistValidatorService(BaseSellerMustNotExistValidatorService):
    def validate(self, seller: SellerEntity | None, user_id: int) -> None:
        if seller is not None:
            raise SellerAlreadyExistsError(user_id=user_id)


class BaseSellerMustExistValidatorService(ABC):
    @abstractmethod
    def validate(self, seller: SellerEntity | None, user_id: int) -> None: ...


class SellerMustExistValidatorService(BaseSellerMustExistValidatorService):
    def validate(self, seller: SellerEntity | None, user_id: int) -> None:
        if seller is None:
            raise SellerNotFoundError(user_id=user_id)


@dataclass
class BaseSellerService(ABC):
    repository: BaseSellerRepository

    @abstractmethod
    def save(self, seller: SellerEntity, update: bool = False) -> SellerEntity: ...

    @abstractmethod
    def try_get_by_id(self, id: int) -> SellerEntity: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class SellerService(BaseSellerService):
    def save(self, seller: SellerEntity, update: bool = False) -> SellerEntity:
        dto = seller_from_entity(entity=seller)
        dto = self.repository.save(seller=dto, update=update)
        return seller_to_entity(dto=dto)

    def try_get_by_id(self, id: int) -> SellerEntity:
        dto = self.repository.get_by_id(id=id)
        if dto is None:
            raise SellerNotFoundByIdError(id=id)
        return seller_to_entity(dto=dto)

    def delete(self, id: int) -> None:
        self.repository.delete(id=id)
