from abc import ABC, abstractmethod

from src.apps.sellers.models import Seller


class BaseSellerRepository(ABC):
    @abstractmethod
    def create(self, dto: Seller) -> Seller: ...


class ORMSellerRepository(BaseSellerRepository):
    def create(self, dto: Seller) -> Seller:
        dto.save()
        return dto
