from abc import ABC, abstractmethod

from src.apps.authentication.exceptions.auth import AuthCredentialsNotProvidedError


class BaseAuthValidatorService(ABC):
    @abstractmethod
    def validate(self, user_id: int | None): ...


class AuthValidatorService(BaseAuthValidatorService):
    def validate(self, user_id: int | None):
        if user_id is None:
            raise AuthCredentialsNotProvidedError
