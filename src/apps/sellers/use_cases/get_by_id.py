from dataclasses import dataclass

from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.services.sellers import BaseSellerService


@dataclass
class GetSellerByIdUseCase:
    seller_service: BaseSellerService

    def execute(self, seller_id: int) -> SellerEntity:
        seller = self.seller_service.get_by_id_or_404(id=seller_id)
        return seller
