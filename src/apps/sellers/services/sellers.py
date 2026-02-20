from abc import ABC, abstractmethod
from dataclasses import dataclass

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


class BaseSellerService(ABC):
    @abstractmethod
    def save(self, seller: SellerEntity, update: bool = False) -> SellerEntity: ...

    @abstractmethod
    def try_get_by_id(self, id: int) -> SellerEntity: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


@dataclass(eq=False)
class SellerService(BaseSellerService):
    repository: BaseSellerRepository

    def save(self, seller: SellerEntity, update: bool = False) -> SellerEntity:
        return self.repository.save(seller=seller, update=update)

    def try_get_by_id(self, id: int) -> SellerEntity:
        seller = self.repository.get_by_id(id=id)
        if seller is None:
            raise SellerNotFoundByIdError(id=id)
        return seller

    def delete(self, id: int) -> None:
        self.repository.delete(id=id)
