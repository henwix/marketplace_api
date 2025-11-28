from dataclasses import dataclass

from src.apps.sellers.models import Seller
from src.apps.sellers.services.sellers import BaseSellerService


@dataclass
class CreateSellerUseCase:
    service: BaseSellerService

    def execute(self, user_id: int, data: dict) -> Seller:
        return self.service.create(user_id=user_id, data=data)
