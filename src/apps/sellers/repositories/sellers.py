from abc import ABC, abstractmethod

from src.apps.sellers.converters.sellers import seller_from_entity, seller_to_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.models import Seller


class BaseSellerRepository(ABC):
    @abstractmethod
    def save(self, seller: SellerEntity, update: bool) -> SellerEntity: ...

    @abstractmethod
    def get_by_id(self, id: int) -> SellerEntity | None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class ORMSellerRepository(BaseSellerRepository):
    def save(self, seller: SellerEntity, update: bool) -> SellerEntity:
        dto = seller_from_entity(entity=seller)
        dto.save(force_update=update)
        return seller_to_entity(dto=dto)

    def get_by_id(self, id: int) -> SellerEntity | None:
        try:
            dto = Seller.objects.get(pk=id)
        except Seller.DoesNotExist:
            return None
        return seller_to_entity(dto=dto)

    def delete(self, id: int) -> None:
        Seller.objects.filter(pk=id).delete()
