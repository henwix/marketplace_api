from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db import IntegrityError

from src.apps.users.exceptions.users import UserWithDataAlreadyExistsError
from src.apps.users.models import User
from src.apps.users.repositories.users import BaseUserRepository


@dataclass
class BaseUserService(ABC):
    repository: BaseUserRepository

    @abstractmethod
    def create(self, data: dict) -> User: ...

    @abstractmethod
    def set_password(self, user: User, password: str) -> None: ...


class UserService(BaseUserService):
    def create(self, data: dict) -> User:
        try:
            return self.repository.create(data=data)
        except IntegrityError:
            raise UserWithDataAlreadyExistsError()

    def set_password(self, user: User, password: str) -> None:
        return self.repository.set_password(user=user, password=password)
