from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db import IntegrityError

from src.apps.users.converters import user_from_entity, user_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import UserWithDataAlreadyExistsError
from src.apps.users.repositories.users import BaseUserRepository


@dataclass
class BaseUserService(ABC):
    repository: BaseUserRepository

    @abstractmethod
    def create(self, data: dict) -> UserEntity: ...

    @abstractmethod
    def save(self, user: UserEntity, update: bool = False) -> UserEntity: ...

    @abstractmethod
    def set_password(self, user: UserEntity, password: str) -> None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class UserService(BaseUserService):
    def create(self, data: dict) -> UserEntity:
        try:
            dto = self.repository.create(data=data)
            return user_to_entity(dto=dto)
        except IntegrityError:
            raise UserWithDataAlreadyExistsError()

    def save(self, user: UserEntity, update: bool = False) -> UserEntity:
        try:
            dto = user_from_entity(entity=user)
            dto = self.repository.save(user=dto, update=update)
            return user_to_entity(dto=dto)
        except IntegrityError:
            raise UserWithDataAlreadyExistsError()

    def set_password(self, user: UserEntity, password: str) -> None:
        dto = user_from_entity(entity=user)
        return self.repository.set_password(user=dto, password=password)

    def delete(self, id: int) -> None:
        self.repository.delete(id=id)
