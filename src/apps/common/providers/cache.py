from abc import ABC, abstractmethod
from typing import Any

from django.core.cache import cache


class BaseCacheProvider(ABC):
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int) -> bool: ...

    @abstractmethod
    def get(self, key: str) -> Any: ...

    @abstractmethod
    def delete(self, key: str) -> bool: ...


class CacheProvider(BaseCacheProvider):
    def set(self, key: str, value: Any, ttl: int | None) -> bool:
        return cache.set(key=key, value=value, timeout=ttl)

    def get(self, key: str) -> Any:
        return cache.get(key=key)

    def delete(self, key: str) -> bool:
        return cache.delete(key=key)
