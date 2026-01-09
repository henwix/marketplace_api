from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db import IntegrityError

from src.apps.users.converters import user_from_entity, user_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
    UserWithDataAlreadyExistsError,
    UserWithEmailAlreadyExistsError,
    UserWithPhoneAlreadyExistsError,
)
from src.apps.users.models import User
from src.apps.users.repositories.users import BaseUserRepository


class BaseUserValidatorService(ABC):
    @abstractmethod
    def validate(self, email: str, phone: str) -> None: ...


@dataclass
class UserUniqueEmailValidatorService(BaseUserValidatorService):
    user_repository: BaseUserRepository

    def validate(self, email: str, *args, **kwargs) -> None:
        if self.user_repository.check_user_with_email_exists(email=email):
            raise UserWithEmailAlreadyExistsError()


@dataclass
class UserUniquePhoneValidatorService(BaseUserValidatorService):
    user_repository: BaseUserRepository

    def validate(self, phone: str, *args, **kwargs) -> None:
        if self.user_repository.check_user_with_phone_exists(phone=phone):
            raise UserWithPhoneAlreadyExistsError()


@dataclass
class ComposedUserValidatorService(BaseUserValidatorService):
    validators: list[BaseUserValidatorService]

    def validate(self, email: str, phone: str) -> None:
        for validator in self.validators:
            validator.validate(email=email, phone=phone)


class BaseUserService(ABC):
    @abstractmethod
    def create(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
    ) -> UserEntity: ...

    @abstractmethod
    def save(self, user: UserEntity, update: bool = False) -> UserEntity: ...

    @abstractmethod
    def try_get_by_id_with_loaded_seller(self, id: int) -> UserEntity: ...

    @abstractmethod
    def try_get_by_id(self, id: int) -> UserEntity: ...

    @abstractmethod
    def set_password(self, user: UserEntity, password: str) -> None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


@dataclass(eq=False)
class UserService(BaseUserService):
    repository: BaseUserRepository

    def _validate_dto_and_convert_to_entity(self, dto: User | None, user_id: int) -> UserEntity:
        if dto is None:
            raise UserNotFoundError(user_id=user_id)
        user = user_to_entity(dto=dto)
        if not user.is_active:
            raise UserNotActiveError(user_id=user_id)
        return user

    def create(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
    ) -> UserEntity:
        try:
            dto = self.repository.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password=password,
            )
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

    def try_get_by_id_with_loaded_seller(self, id: int) -> UserEntity:
        dto = self.repository.get_by_id_with_loaded_seller(id=id)
        return self._validate_dto_and_convert_to_entity(dto=dto, user_id=id)

    def try_get_by_id(self, id: int) -> UserEntity:
        dto = self.repository.get_by_id(id=id)
        return self._validate_dto_and_convert_to_entity(dto=dto, user_id=id)

    def set_password(self, user: UserEntity, password: str) -> None:
        dto = user_from_entity(entity=user)
        return self.repository.set_password(user=dto, password=password)

    def delete(self, id: int) -> None:
        self.repository.delete(id=id)
