from abc import ABC, abstractmethod

from src.apps.sellers.models import Seller


class BaseSellerRepository(ABC):
    @abstractmethod
    def save(self, seller: Seller, update: bool) -> Seller: ...

    @abstractmethod
    def get_by_id(self, id: int) -> Seller | None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class ORMSellerRepository(BaseSellerRepository):
    def save(self, seller: Seller, update: bool) -> Seller:
        seller.save(force_update=update)
        return seller

    def get_by_id(self, id: int) -> Seller | None:
        return Seller.objects.filter(pk=id).first()

    def delete(self, id: int) -> None:
        Seller.objects.filter(pk=id).delete()
