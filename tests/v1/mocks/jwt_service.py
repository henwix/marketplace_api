from dataclasses import dataclass, field

from src.apps.authentication.exceptions.jwt import JWTTokenInvalidError
from src.apps.authentication.services.jwt import BaseJWTService
from src.apps.users.entities import UserEntity


@dataclass
class DummyJWTService(BaseJWTService):
    EXPECTED_TOKEN_PAYLOAD: dict[str, str] = field(default_factory=dict)
    RAISE_DECODE_EXCEPTION: bool = False

    def create_tokens(self, user: UserEntity) -> dict:
        return {}

    def decode_unverified(self, token: str) -> dict[str, str]:
        if self.RAISE_DECODE_EXCEPTION is True:
            raise JWTTokenInvalidError(error_details='test')
        return self.EXPECTED_TOKEN_PAYLOAD
