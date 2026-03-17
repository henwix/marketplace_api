from abc import ABC, abstractmethod


class BaseOAuthService(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str: ...

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
