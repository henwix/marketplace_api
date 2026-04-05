from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.authentication.constants import SupportedAuthProviders
from src.apps.authentication.entities.auth_providers import AuthProviderEntity
from src.apps.authentication.exceptions.auth_providers import (
    AuthProviderNotConnectedError,
    AuthProviderNotSupportedError,
)
from src.apps.authentication.repositories.auth_providers import BaseAuthProviderRepository


class BaseAuthProviderMustExistValidatorService(ABC):
    @abstractmethod
    def validate(self, provider: str) -> None: ...


class AuthProviderMustExistValidatorService(BaseAuthProviderMustExistValidatorService):
    def validate(self, provider: str) -> None:
        if provider not in SupportedAuthProviders:
            raise AuthProviderNotSupportedError(provider=provider)


class BaseAuthProviderService(ABC):
    @abstractmethod
    def get_by_provider_uid_and_name(self, provider_uid: str, provider: str) -> AuthProviderEntity: ...

    @abstractmethod
    def get_many_by_user_id(self, user_id: int) -> list[AuthProviderEntity]: ...

    @abstractmethod
    def get_many_by_user_id_for_update(self, user_id: int) -> list[AuthProviderEntity]: ...

    @abstractmethod
    def save(self, auth_provider: AuthProviderEntity, update: bool) -> AuthProviderEntity: ...

    @abstractmethod
    def try_delete_by_user_id_and_provider(self, user_id: int, provider: str) -> None: ...


@dataclass(eq=False)
class AuthProviderService(BaseAuthProviderService):
    repository: BaseAuthProviderRepository

    def get_by_provider_uid_and_name(self, provider_uid: str, provider: str) -> AuthProviderEntity | None:
        return self.repository.get_by_provider_uid_and_name(provider_uid=provider_uid, provider=provider)

    def get_many_by_user_id(self, user_id: int) -> list[AuthProviderEntity]:
        return self.repository.get_many_by_user_id(user_id=user_id)

    def get_many_by_user_id_for_update(self, user_id: int) -> list[AuthProviderEntity]:
        return self.repository.get_many_by_user_id_for_update(user_id=user_id)

    def save(self, auth_provider: AuthProviderEntity, update: bool) -> AuthProviderEntity:
        return self.repository.save(auth_provider=auth_provider, update=update)

    def try_delete_by_user_id_and_provider(self, user_id: int, provider: str) -> None:
        is_deleted = self.repository.delete_by_user_id_and_provider(user_id=user_id, provider=provider)
        if not is_deleted:
            raise AuthProviderNotConnectedError(user_id=user_id, provider=provider)
