from punq import Container

from src.apps.common.clients.http_client import BaseHTTPClient, HTTPClient
from src.apps.common.providers.cache import BaseCacheProvider, CacheProvider


def init_common(container: Container) -> None:
    # providers
    container.register(BaseCacheProvider, CacheProvider)

    # clients
    container.register(BaseHTTPClient, HTTPClient)
