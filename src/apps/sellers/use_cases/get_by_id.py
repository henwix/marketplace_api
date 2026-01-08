from dataclasses import dataclass

from src.apps.sellers.commands import GetSellerByIdCommand
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.services.sellers import BaseSellerService


@dataclass(eq=False)
class GetSellerByIdUseCase:
    seller_service: BaseSellerService

    def execute(self, command: GetSellerByIdCommand) -> SellerEntity:
        seller = self.seller_service.try_get_by_id(id=command.seller_id)
        return seller
