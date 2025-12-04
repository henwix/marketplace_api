from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.sellers.converters.sellers import seller_from_entity, seller_to_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.repositories.sellers import BaseSellerRepository


@dataclass
class BaseSellerService(ABC):
    repository: BaseSellerRepository

    @abstractmethod
    def create(self, entity: SellerEntity) -> SellerEntity: ...


class SellerService(BaseSellerService):
    def create(self, entity: SellerEntity) -> SellerEntity:
        dto = seller_from_entity(entity=entity)
        dto = self.repository.create(dto=dto)
        return seller_to_entity(dto=dto)
