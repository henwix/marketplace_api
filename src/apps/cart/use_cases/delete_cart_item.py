from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.cart.commands import DeleteCartItemCommand
from src.apps.cart.services.cart import BaseCartService
from src.apps.users.services.users import BaseUserService


@dataclass
class DeleteCartItemUseCase:
    auth_validator_service: BaseAuthValidatorService
    user_service: BaseUserService
    cart_service: BaseCartService

    def execute(self, command: DeleteCartItemCommand) -> None:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        cart = self.cart_service.get_or_create_cart(user_id=user.id)
        self.cart_service.try_delete_cart_item(cart_id=cart.id, product_variant_id=command.product_variant_id)
