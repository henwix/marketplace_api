from dataclasses import dataclass

from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.services.sellers import BaseSellerService


@dataclass
class GetSellerByIdUseCase:
    seller_service: BaseSellerService

    def execute(self, seller_id: int) -> SellerEntity:
        seller = self.seller_service.try_get_by_id(id=seller_id)
        return seller
