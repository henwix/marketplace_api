from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.sellers.models import Seller
from src.apps.sellers.repositories.sellers import BaseSellerRepository


@dataclass
class BaseSellerService(ABC):
    repository: BaseSellerRepository

    @abstractmethod
    def create(self, user_id: int, data: dict) -> Seller: ...


class SellerService(BaseSellerService):
    def create(self, user_id: int, data: dict) -> Seller:
        data.update({'user_id': user_id})
        return self.repository.create(data=data)
