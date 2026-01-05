from collections.abc import Iterable
from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.products.commands.products import PersonalSearchProductCommand
from src.apps.products.models.products import Product
from src.apps.products.services.products import BaseProductService
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService
from src.apps.users.services.users import BaseUserService


@dataclass
class PersonalSearchProductUseCase:
    user_service: BaseUserService
    product_service: BaseProductService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService

    def execute(self, command: PersonalSearchProductCommand) -> Iterable[Product]:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=command.user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        products = self.product_service.get_many_for_personal_search(seller_id=user.seller_profile.id)
        return products
