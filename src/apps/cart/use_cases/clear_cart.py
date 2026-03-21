from dataclasses import dataclass

from django.db import transaction

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.cart.commands import ClearCartCommand
from src.apps.cart.services.cart import BaseCartService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class ClearCartUseCase:
    auth_validator_service: BaseAuthValidatorService
    user_service: BaseUserService
    cart_service: BaseCartService

    def execute(self, command: ClearCartCommand) -> None:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        with transaction.atomic():
            cart = self.cart_service.get_or_create_cart_by_user_id_for_update(user_id=user.id)
            self.cart_service.try_clear_cart(cart_id=cart.id)
