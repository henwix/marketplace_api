from src.apps.authentication.entities.auth_providers import AuthProviderEntity
from src.apps.authentication.models.auth_provider import AuthProvider


def auth_provider_to_entity(dto: AuthProvider) -> AuthProviderEntity:
    return AuthProviderEntity(
        id=dto.pk,
        user_id=dto.user_id,
        provider=dto.provider,
        provider_uid=dto.provider_uid,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
    )


def auth_provider_from_entity(entity: AuthProviderEntity) -> AuthProvider:
    return AuthProvider(
        pk=entity.id,
        user_id=entity.user_id,
        provider=entity.provider,
        provider_uid=entity.provider_uid,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
