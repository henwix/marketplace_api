from dataclasses import dataclass

from src.apps.authentication.services.oauth.factory import BaseOAuthServiceFactory
from src.apps.authentication.services.oauth.service import BaseOAuthService
from tests.v1.authentication.oauth.mocks.service import DummyOAuthService


@dataclass
class DummyOAuthServiceFactory(BaseOAuthServiceFactory):
    service: BaseOAuthService | None = None

    def get(self, provider_name: str) -> BaseOAuthService:
        return self.service or DummyOAuthService()
