from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.cart.commands import GetCartCommand
from src.apps.cart.entities import CartItemEntity
from src.apps.cart.exceptions import CartEmptyError
from src.apps.cart.services.cart import BaseCartService
from src.apps.users.services.users import BaseUserService


@dataclass(eq=False)
class GetCartUseCase:
    auth_validator_service: BaseAuthValidatorService
    user_service: BaseUserService
    cart_service: BaseCartService

    def execute(self, command: GetCartCommand) -> tuple[list[CartItemEntity], Decimal, int]:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_active_by_id(id=command.user_id)
        with transaction.atomic():
            cart = self.cart_service.get_or_create_cart_by_user_id_for_update(user_id=user.id)
            cart_items = self.cart_service.get_cart_items_by_cart_id(cart_id=cart.id)
            if not cart_items:
                raise CartEmptyError(cart_id=cart.id)
            total_cart_price = self.cart_service.get_total_cart_price(cart_id=cart.id)
            cart_items_count = self.cart_service.get_cart_items_count(cart_id=cart.id)
            return cart_items, total_cart_price, cart_items_count
