from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.authentication.entities.social_account import SocialAccountEntity
from src.apps.authentication.repositories.social_account import BaseSocialAccountRepository


class BaseSocialAccountService(ABC):
    @abstractmethod
    def get_by_provider_uid_and_name(self, provider_uid: str, provider: str) -> SocialAccountEntity: ...

    @abstractmethod
    def save(self, social_account: SocialAccountEntity, update: bool) -> SocialAccountEntity: ...


@dataclass(eq=False)
class SocialAccountService(BaseSocialAccountService):
    repository: BaseSocialAccountRepository

    def get_by_provider_uid_and_name(self, provider_uid: str, provider: str) -> SocialAccountEntity | None:
        return self.repository.get_by_provider_uid_and_name(provider_uid=provider_uid, provider=provider)

    def save(self, social_account: SocialAccountEntity, update: bool) -> SocialAccountEntity:
        return self.repository.save(social_account=social_account, update=update)
