from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db import IntegrityError

from src.apps.users.converters import user_from_entity, user_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import (
    UserAuthCredentialsNotProvidedError,
    UserAuthNotActiveError,
    UserAuthNotFoundError,
    UserWithDataAlreadyExistsError,
)
from src.apps.users.models import User
from src.apps.users.repositories.users import BaseUserRepository


class BaseUserAuthValidatorService(ABC):
    @abstractmethod
    def validate(self, user_id: int | None): ...


class UserAuthValidatorService(BaseUserAuthValidatorService):
    def validate(self, user_id: int | None):
        if user_id is None:
            raise UserAuthCredentialsNotProvidedError()


@dataclass
class BaseUserService(ABC):
    repository: BaseUserRepository

    @abstractmethod
    def create(self, data: dict) -> UserEntity: ...

    @abstractmethod
    def save(self, user: UserEntity, update: bool = False) -> UserEntity: ...

    @abstractmethod
    def get_by_id_with_seller_or_401(self, id: int) -> UserEntity: ...

    @abstractmethod
    def get_by_id_or_401(self, id: int) -> UserEntity: ...

    @abstractmethod
    def set_password(self, user: UserEntity, password: str) -> None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


class UserService(BaseUserService):
    def _validate_dto_and_convert_to_entity(self, dto: User | None, user_id: int) -> UserEntity:
        if dto is None:
            raise UserAuthNotFoundError(user_id=user_id)
        user = user_to_entity(dto=dto)
        if not user.is_active:
            raise UserAuthNotActiveError(user_id=user_id)
        return user

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

    def get_by_id_with_seller_or_401(self, id: int) -> UserEntity:
        dto = self.repository.get_by_id_with_seller_or_none(id=id)
        return self._validate_dto_and_convert_to_entity(dto=dto, user_id=id)

    def get_by_id_or_401(self, id: int) -> UserEntity:
        dto = self.repository.get_by_id_or_none(id=id)
        return self._validate_dto_and_convert_to_entity(dto=dto, user_id=id)

    def set_password(self, user: UserEntity, password: str) -> None:
        dto = user_from_entity(entity=user)
        return self.repository.set_password(user=dto, password=password)

    def delete(self, id: int) -> None:
        self.repository.delete(id=id)
