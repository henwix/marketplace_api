from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.sellers.converters.sellers import seller_from_entity, seller_to_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.exceptions import SellerAlreadyExistsError, SellerNotFoundByIdError, SellerNotFoundError
from src.apps.sellers.repositories.sellers import BaseSellerRepository


class BaseSellerAlreadyExistsValidatorService(ABC):
    @abstractmethod
    def validate(self, seller: SellerEntity | None, user_id: int) -> None: ...


class SellerAlreadyExistsValidatorService(BaseSellerAlreadyExistsValidatorService):
    def validate(self, seller: SellerEntity | None, user_id: int) -> None:
        if seller is not None:
            raise SellerAlreadyExistsError(user_id=user_id)


class BaseSellerDoesNotExistValidatorService(ABC):
    @abstractmethod
    def validate(self, seller: SellerEntity | None, user_id: int) -> None: ...


class SellerDoesNotExistValidatorService(BaseSellerDoesNotExistValidatorService):
    def validate(self, seller: SellerEntity | None, user_id: int) -> None:
        if seller is None:
            raise SellerNotFoundError(user_id=user_id)


@dataclass
class BaseSellerService(ABC):
    repository: BaseSellerRepository

    @abstractmethod
    def save(self, seller: SellerEntity, update: bool = False) -> SellerEntity: ...

    @abstractmethod
    def get_by_user_id_or_none(self, user_id: int) -> SellerEntity | None: ...

    @abstractmethod
    def get_by_user_id_or_404(self, user_id: int) -> SellerEntity: ...

    @abstractmethod
    def get_by_id_or_404(self, id: int) -> SellerEntity: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class SellerService(BaseSellerService):
    def save(self, seller: SellerEntity, update: bool = False) -> SellerEntity:
        dto = seller_from_entity(entity=seller)
        dto = self.repository.save(seller=dto, update=update)
        return seller_to_entity(dto=dto)

    def get_by_user_id_or_none(self, user_id: int) -> SellerEntity | None:
        dto = self.repository.get_by_user_id_or_none(user_id=user_id)
        return dto if dto is None else seller_to_entity(dto=dto)

    def get_by_user_id_or_404(self, user_id: int) -> SellerEntity:
        dto = self.repository.get_by_user_id_or_none(user_id=user_id)
        if dto is None:
            raise SellerNotFoundError(user_id=user_id)
        return seller_to_entity(dto=dto)

    def get_by_id_or_404(self, id: int) -> SellerEntity:
        dto = self.repository.get_by_id_or_none(id=id)
        if dto is None:
            raise SellerNotFoundByIdError(id=id)
        return seller_to_entity(dto=dto)

    def delete(self, id: int) -> None:
        self.repository.delete(id=id)
