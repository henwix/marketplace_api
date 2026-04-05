from dataclasses import dataclass
from datetime import datetime

from src.apps.common.entities import BaseEntity


@dataclass(kw_only=True)
class AuthProviderEntity(BaseEntity):
    id: int | None = None
    user_id: int
    provider: str
    provider_uid: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @staticmethod
    def create(user_id: int, provider: str, provider_uid: str) -> AuthProviderEntity:
        return AuthProviderEntity(
            user_id=user_id,
            provider=provider,
            provider_uid=provider_uid,
        )
