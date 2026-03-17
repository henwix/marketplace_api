from abc import ABC, abstractmethod

from django.db import IntegrityError

from src.apps.authentication.converters.social_account import social_account_from_entity, social_account_to_entity
from src.apps.authentication.entities.social_account import SocialAccountEntity
from src.apps.authentication.exceptions.social_account import SocialAccountProviderAlreadyConnectedError
from src.apps.authentication.models.social_account import SocialAccount


class BaseSocialAccountRepository(ABC):
    @abstractmethod
    def get_by_provider_uid_and_name(self, provider_uid: str, provider: str) -> SocialAccountEntity | None: ...

    @abstractmethod
    def save(self, social_account: SocialAccountEntity, update: bool) -> SocialAccountEntity: ...


class ORMSocialAccountRepository(BaseSocialAccountRepository):
    def get_by_provider_uid_and_name(self, provider_uid: str, provider: str) -> SocialAccountEntity | None:
        dto = SocialAccount.objects.filter(provider_uid=provider_uid, provider=provider).first()
        return social_account_to_entity(dto=dto) if dto else None

    def save(self, social_account: SocialAccountEntity, update: bool) -> SocialAccountEntity:
        dto = social_account_from_entity(entity=social_account)
        try:
            dto.save(force_update=update)
        except IntegrityError as error:
            raise SocialAccountProviderAlreadyConnectedError(
                current_user_id=social_account.user_id,
                provider=social_account.provider,
            ) from error
        return social_account_to_entity(dto=dto)
