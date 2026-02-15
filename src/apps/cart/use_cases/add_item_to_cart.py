from dataclasses import dataclass

from src.apps.authentication.services.auth import BaseAuthValidatorService
from src.apps.cart.commands import AddItemToCartCommand
from src.apps.cart.entities import CartItemEntity
from src.apps.cart.services.cart import (
    BaseCartItemMustNotExistInCartValidatorService,
    BaseCartService,
)
from src.apps.products.services.product_variants import (
    BaseProductVariantService,
    BaseProductVariantStockValidatorService,
    BaseProductVariantVisibilityValidatorService,
)
from src.apps.users.services.users import BaseUserService


@dataclass
class AddItemToCartUseCase:
    user_service: BaseUserService
    product_variant_service: BaseProductVariantService
    product_variant_visiblity_validator_service: BaseProductVariantVisibilityValidatorService
    product_variant_stock_validator_service: BaseProductVariantStockValidatorService
    cart_service: BaseCartService
    cart_item_must_not_exist_validator_service: BaseCartItemMustNotExistInCartValidatorService
    auth_validator_service: BaseAuthValidatorService

    def execute(self, command: AddItemToCartCommand) -> CartItemEntity:
        self.auth_validator_service.validate(user_id=command.user_id)
        user = self.user_service.try_get_by_id(id=command.user_id)
        product_variant = self.product_variant_service.try_get_by_id_with_loaded_product(id=command.product_variant_id)
        cart = self.cart_service.get_or_create_cart(user_id=user.id)
        self.cart_item_must_not_exist_validator_service.validate(cart=cart, product_variant=product_variant)
        self.product_variant_visiblity_validator_service.validate(product_variant=product_variant)
        self.product_variant_stock_validator_service.validate(
            product_variant=product_variant, quantity=command.quantity
        )
        cart_item_entity = CartItemEntity.create(
            cart_id=cart.id,
            product_variant_id=product_variant.id,
            seller_id=product_variant.product_seller_id,
            quantity=command.quantity,
            price_snapshot=product_variant.price,
        )
        new_cart_item = self.cart_service.save_cart_item(cart_item=cart_item_entity, update=False)
        return new_cart_item
