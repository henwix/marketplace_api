from abc import ABC, abstractmethod


class BaseOAuthProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str: ...

    @abstractmethod
    def exchange_code(self, code: str) -> str: ...

    @abstractmethod
    def get_user_data(self, token: str) -> dict: ...

    @abstractmethod
    def get_login_url(self, state: str) -> str: ...
