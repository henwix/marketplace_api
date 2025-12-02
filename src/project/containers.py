from functools import lru_cache
from logging import Logger, getLogger

import punq

from src.apps.products.containers import init_products
from src.apps.sellers.containers import init_sellers
from src.apps.users.containers import init_users


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    init_users(container=container)
    init_sellers(container=container)
    init_products(container=container)
    container.register(Logger, factory=getLogger, name='django.logger')

    return container
