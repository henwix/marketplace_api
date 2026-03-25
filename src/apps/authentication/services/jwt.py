from abc import ABC, abstractmethod

from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.users.converters import user_from_entity
from src.apps.users.entities import UserEntity


class BaseJWTService(ABC):
    @abstractmethod
    def create_tokens(self, user: UserEntity) -> dict: ...


class JWTService(BaseJWTService):
    def create_tokens(self, user: UserEntity) -> dict:
        refresh = RefreshToken.for_user(user=user_from_entity(entity=user))
        access = refresh.access_token
        return {'refresh': str(refresh), 'access': str(access)}
