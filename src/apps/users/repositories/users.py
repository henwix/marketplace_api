from abc import ABC, abstractmethod

from src.apps.users.models import User


class BaseUserRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> User: ...

    @abstractmethod
    def set_password(self, user: User, password: str) -> None: ...


class ORMUserRepository(BaseUserRepository):
    def create(self, data: dict) -> User:
        return User.objects.create_user(**data)

    def set_password(self, user: User, password: str) -> None:
        user.set_password(password)
        user.save()
