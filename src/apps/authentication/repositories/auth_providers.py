from abc import ABC, abstractmethod
from collections.abc import Iterable

from django.db import IntegrityError

from src.apps.authentication.converters.auth_providers import auth_provider_from_entity, auth_provider_to_entity
from src.apps.authentication.entities.auth_providers import AuthProviderEntity
from src.apps.authentication.exceptions.auth_providers import AuthProviderAlreadyConnectedError
from src.apps.authentication.models.auth_provider import AuthProvider


class BaseAuthProviderRepository(ABC):
    @abstractmethod
    def get_by_provider_uid_and_name(self, provider_uid: str, provider: str) -> AuthProviderEntity | None: ...

    @abstractmethod
    def get_many_by_user_id(self, user_id: int) -> list[AuthProviderEntity]: ...

    @abstractmethod
    def get_many_by_user_id_for_update(self, user_id: int) -> list[AuthProviderEntity]: ...

    @abstractmethod
    def save(self, auth_provider: AuthProviderEntity, update: bool) -> AuthProviderEntity: ...

    @abstractmethod
    def delete_by_user_id_and_provider(self, user_id: int, provider: str) -> bool: ...


class ORMAuthProviderRepository(BaseAuthProviderRepository):
    def _many_to_entity(self, auth_providers: Iterable[AuthProvider]) -> list[AuthProviderEntity]:
        if auth_providers:
            return [auth_provider_to_entity(dto=dto) for dto in auth_providers]
        return []

    def get_by_provider_uid_and_name(self, provider_uid: str, provider: str) -> AuthProviderEntity | None:
        try:
            dto = AuthProvider.objects.get(provider_uid=provider_uid, provider=provider)
        except AuthProvider.DoesNotExist:
            return None
        return auth_provider_to_entity(dto=dto)

    def get_many_by_user_id(self, user_id: int) -> list[AuthProviderEntity]:
        auth_providers = AuthProvider.objects.filter(user_id=user_id)
        return self._many_to_entity(auth_providers=auth_providers)

    def get_many_by_user_id_for_update(self, user_id: int) -> list[AuthProviderEntity]:
        auth_providers = AuthProvider.objects.select_for_update().filter(user_id=user_id)
        return self._many_to_entity(auth_providers=auth_providers)

    def save(self, auth_provider: AuthProviderEntity, update: bool) -> AuthProviderEntity:
        dto = auth_provider_from_entity(entity=auth_provider)
        try:
            dto.save(force_update=update)
        except IntegrityError as error:
            raise AuthProviderAlreadyConnectedError(
                current_user_id=auth_provider.user_id,
                provider=auth_provider.provider,
            ) from error
        return auth_provider_to_entity(dto=dto)

    def delete_by_user_id_and_provider(self, user_id: int, provider: str) -> bool:
        return AuthProvider.objects.filter(user_id=user_id, provider=provider).delete()[0] > 0
