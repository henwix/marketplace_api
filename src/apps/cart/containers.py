from punq import Container

from src.apps.cart.repositories.cart import BaseCartRepository, CartRepository
from src.apps.cart.services.cart import BaseCartService, CartService
from src.apps.cart.use_cases.add_item_to_cart import AddItemToCartUseCase


def init_cart(container: Container) -> Container:
    # use_cases
    container.register(AddItemToCartUseCase)

    # services
    container.register(BaseCartService, CartService)

    # repositories
    container.register(BaseCartRepository, CartRepository)
