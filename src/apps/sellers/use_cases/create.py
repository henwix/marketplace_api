from dataclasses import dataclass

from src.apps.sellers.converters.sellers import data_to_seller_entity
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.services.sellers import BaseSellerService


@dataclass
class CreateSellerUseCase:
    service: BaseSellerService

    def execute(self, user_id: int, data: dict) -> SellerEntity:
        seller_entity = data_to_seller_entity(data={**data, 'user_id': user_id})
        new_seller = self.service.create(entity=seller_entity)
        return new_seller
