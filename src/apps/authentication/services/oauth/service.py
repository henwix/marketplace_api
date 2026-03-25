from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import uuid4

from src.apps.authentication.exceptions.oauth import OAuthIncorrectStateError
from src.apps.authentication.providers.oauth.base import BaseOAuthProvider
from src.apps.common.providers.cache import BaseCacheProvider


class BaseOAuthService(ABC):
    @abstractmethod
    def create_state(self) -> str: ...

    @abstractmethod
    def validate_state(self, state: str) -> None: ...

    @abstractmethod
    def exchange_code(self, code: str) -> str: ...

    @abstractmethod
    def get_user_data(self, token: str) -> dict: ...

    @abstractmethod
    def get_login_url(self) -> str: ...


@dataclass(eq=False)
class OAuthService(BaseOAuthService):
    cache_provider: BaseCacheProvider
    oauth_provider: BaseOAuthProvider

    def _make_state_key(self, state: str) -> str:
        return f'oauth:state:{self.oauth_provider.provider_name}:{state}'

    def create_state(self) -> str:
        state = uuid4().hex
        self.cache_provider.set(key=self._make_state_key(state=state), value=state, ttl=60 * 10)
        return state

    def validate_state(self, state: str) -> None:
        cached_state = self.cache_provider.get(key=self._make_state_key(state=state))
        if cached_state is None:
            raise OAuthIncorrectStateError(state=state)
        self.cache_provider.delete(key=self._make_state_key(state=state))

    def exchange_code(self, code: str) -> str:
        return self.oauth_provider.exchange_code(code=code)

    def get_user_data(self, token: str) -> dict[str, str]:
        return self.oauth_provider.get_user_data(token=token)

    def get_login_url(self) -> str:
        return self.oauth_provider.get_login_url(state=self.create_state())
