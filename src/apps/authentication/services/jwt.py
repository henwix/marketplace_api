from abc import ABC, abstractmethod

import jwt
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.authentication.exceptions.jwt import JWTTokenInvalidError
from src.apps.users.converters import user_from_entity
from src.apps.users.entities import UserEntity


class BaseJWTService(ABC):
    @abstractmethod
    def create_tokens(self, user: UserEntity) -> dict: ...

    @abstractmethod
    def decode_unverified(self, token: str) -> dict[str, str]: ...


class JWTService(BaseJWTService):
    def create_tokens(self, user: UserEntity) -> dict:
        refresh = RefreshToken.for_user(user=user_from_entity(entity=user))
        access = refresh.access_token
        return {'refresh': str(refresh), 'access': str(access)}

    def decode_unverified(
        self,
        token: str,
    ) -> dict[str, str]:
        try:
            payload = jwt.decode(jwt=token, options={'verify_signature': False})
        except jwt.InvalidTokenError as exc:
            raise JWTTokenInvalidError(error_details=str(exc)) from exc
        return payload
