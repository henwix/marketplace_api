from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.cart.commands import AddItemToCartCommand
from src.apps.cart.models import CartItem
from src.apps.cart.services.cart import BaseCartService
from src.apps.products.services.product_variants import BaseProductVariantService
from src.apps.users.services.users import BaseUserService


@dataclass
class AddItemToCartUseCase:
    user_service: BaseUserService
    product_variant_service: BaseProductVariantService
    cart_service: BaseCartService
    auth_validator_service: BaseAuthValidatorService

    def execute(self, command: AddItemToCartCommand) -> None:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id(id=command.user_id)
        product_variant = self.product_variant_service.try_get_by_id_with_loaded_product(id=command.product_variant_id)
        cart = self.cart_service.get_or_create(user_id=user.id)
        # create Cart service + repo, use entities
        # check that variant stock > 0 and quantity >= 0
        # check that variant is visible
        # check that variant does not exists in cart
        CartItem.objects.create(
            cart_id=cart.id,
            product_variant_id=product_variant.id,
            seller_id=product_variant.product_seller_id,
            quantity=command.quantity,
            price_snapshot=product_variant.price,
        )
