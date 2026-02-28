from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.cart.commands import GetCartCommand
from src.apps.cart.exceptions import CartIsEmptyError
from src.apps.cart.services.cart import BaseCartService
from src.apps.users.services.users import BaseUserService


@dataclass
class GetCartUseCase:
    auth_validator_service: BaseAuthValidatorService
    user_service: BaseUserService
    cart_service: BaseCartService

    def execute(self, command: GetCartCommand) -> tuple[Iterable, Decimal, int]:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id(id=command.user_id)
        with transaction.atomic():
            cart = self.cart_service.get_or_create_cart_for_update(user_id=user.id)
            cart_items = self.cart_service.get_cart_items_by_cart_id(cart_id=cart.id)
            if not cart_items:
                raise CartIsEmptyError(cart_id=cart.id)
            total_cart_price = self.cart_service.get_total_cart_price(cart_id=cart.id)
            cart_items_count = self.cart_service.get_cart_items_count(cart_id=cart.id)
            return cart_items, total_cart_price, cart_items_count
