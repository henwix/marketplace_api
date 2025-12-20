from abc import ABC, abstractmethod

from src.apps.users.models import User


class BaseUserRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> User: ...

    @abstractmethod
    def save(self, user: User, update: bool) -> User: ...

    @abstractmethod
    def set_password(self, user: User, password: str) -> None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class ORMUserRepository(BaseUserRepository):
    def create(self, data: dict) -> User:
        return User.objects.create_user(**data)

    def save(self, user: User, update: bool) -> User:
        user.save(force_update=update)
        return user

    def set_password(self, user: User, password: str) -> None:
        user.set_password(password)
        user.save()

    def delete(self, id: int) -> None:
        User.objects.filter(pk=id).delete()
