from functools import lru_cache
from logging import Logger, getLogger

from punq import Container

from src.apps.authentication.containers import init_auth
from src.apps.cart.containers import init_cart
from src.apps.products.containers import init_products
from src.apps.sellers.containers import init_sellers
from src.apps.users.containers import init_users


def resolve_depends(interface):
    return get_container().resolve(interface)


@lru_cache(1)
def get_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    init_users(container=container)
    init_sellers(container=container)
    init_products(container=container)
    init_cart(container=container)
    init_auth(container=container)
    container.register(Logger, factory=getLogger, name='django.logger')

    return container
