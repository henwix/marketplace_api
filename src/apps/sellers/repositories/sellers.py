from abc import ABC, abstractmethod

from src.apps.sellers.models import Seller


class BaseSellerRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> Seller: ...


class ORMSellerRepository(BaseSellerRepository):
    def create(self, data: dict) -> Seller:
        return Seller.objects.create(**data)
