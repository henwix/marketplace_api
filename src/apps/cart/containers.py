from punq import Container

from src.apps.cart.repositories.cart import BaseCartRepository, CartRepository
from src.apps.cart.services.cart import (
    BaseCartItemMustNotExistInCartValidatorService,
    BaseCartLimitValidatorService,
    BaseCartService,
    CartItemMustNotExistInCartValidatorService,
    CartLimitValidatorService,
    CartService,
)
from src.apps.cart.use_cases.add_cart_item import AddCartItemUseCase
from src.apps.cart.use_cases.clear_cart import ClearCartUseCase
from src.apps.cart.use_cases.delete_cart_item import DeleteCartItemUseCase
from src.apps.cart.use_cases.get_cart import GetCartUseCase


def init_cart(container: Container) -> Container:
    # use_cases
    container.register(AddCartItemUseCase)
    container.register(GetCartUseCase)
    container.register(DeleteCartItemUseCase)
    container.register(ClearCartUseCase)

    # services
    container.register(BaseCartService, CartService)
    container.register(BaseCartItemMustNotExistInCartValidatorService, CartItemMustNotExistInCartValidatorService)
    container.register(BaseCartLimitValidatorService, CartLimitValidatorService)

    # repositories
    container.register(BaseCartRepository, CartRepository)
