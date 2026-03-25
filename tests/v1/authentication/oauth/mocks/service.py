from dataclasses import dataclass, field
from uuid import uuid4

from src.apps.authentication.services.oauth.service import BaseOAuthService


@dataclass
class DummyOAuthService(BaseOAuthService):
    state: str = ''
    token: str = ''
    user_data: dict = field(default_factory=dict)
    login_url: str = ''

    def create_state(self) -> str:
        return self.state or uuid4().hex

    def validate_state(self, state: str) -> None: ...

    def exchange_code(self, code: str) -> str:
        return self.token or uuid4().hex

    def get_user_data(self, token: str) -> dict:
        return self.user_data or {
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'test@example.com',
            'provider_uid': uuid4().hex[:11],
            'avatar': 'https://avatar.example.com',
        }

    def get_login_url(self) -> str:
        return self.login_url or 'https://example.com/login'
