from src.apps.authentication.entities.social_account import SocialAccountEntity
from src.apps.authentication.models.social_account import SocialAccount


def social_account_to_entity(dto: SocialAccount) -> SocialAccountEntity:
    return SocialAccountEntity(
        id=dto.pk,
        user_id=dto.user_id,
        provider=dto.provider,
        provider_uid=dto.provider_uid,
        created_at=dto.created_at,
        updated_at=dto.updated_at,
    )


def social_account_from_entity(entity: SocialAccountEntity) -> SocialAccount:
    return SocialAccount(
        pk=entity.id,
        user_id=entity.user_id,
        provider=entity.provider,
        provider_uid=entity.provider_uid,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
