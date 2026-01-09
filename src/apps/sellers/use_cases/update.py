from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.sellers.commands import UpdateSellerCommand
from src.apps.sellers.entities.sellers import SellerEntity
from src.apps.sellers.services.sellers import BaseSellerMustExistValidatorService, BaseSellerService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class UpdateSellerUseCase:
    user_service: BaseUserService
    seller_service: BaseSellerService
    auth_validator_service: BaseAuthValidatorService
    seller_validator_service: BaseSellerMustExistValidatorService

    def execute(self, command: UpdateSellerCommand) -> SellerEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id_with_loaded_seller(id=command.user_id)
        self.seller_validator_service.validate(seller=user.seller_profile, user_id=user.id)
        user.seller_profile.update_fields(
            name=command.name,
            description=command.description,
        )
        return self.seller_service.save(seller=user.seller_profile, update=True)
