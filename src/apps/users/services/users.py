from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.apps.common.types import UNSET, Unset
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import (
    UserNotActiveError,
    UserNotFoundError,
    UserWithEmailAlreadyExistsError,
    UserWithPhoneAlreadyExistsError,
)
from src.apps.users.repositories.users import BaseUserRepository


class BaseUserValidatorService(ABC):
    @abstractmethod
    def validate(self, email: str | Unset, phone: str | Unset) -> None: ...


@dataclass
class UserUniqueEmailValidatorService(BaseUserValidatorService):
    user_repository: BaseUserRepository

    def validate(self, email: str | Unset, *args, **kwargs) -> None:
        if email is not UNSET and self.user_repository.check_user_with_email_exists(email=email):
            raise UserWithEmailAlreadyExistsError


@dataclass
class UserUniquePhoneValidatorService(BaseUserValidatorService):
    user_repository: BaseUserRepository

    def validate(self, phone: str | Unset, *args, **kwargs) -> None:
        if phone is not UNSET and self.user_repository.check_user_with_phone_exists(phone=phone):
            raise UserWithPhoneAlreadyExistsError


@dataclass
class ComposedUserValidatorService(BaseUserValidatorService):
    validators: list[BaseUserValidatorService]

    def validate(self, email: str | Unset, phone: str | Unset) -> None:
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
    def try_get_active_by_id(self, id: int) -> UserEntity: ...

    @abstractmethod
    def set_password(self, user: UserEntity, password: str) -> None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...


@dataclass(eq=False)
class UserService(BaseUserService):
    repository: BaseUserRepository

    def _validate_user(self, user: UserEntity | None, user_id: int) -> None:
        if user is None:
            raise UserNotFoundError(user_id=user_id)
        if not user.is_active:
            raise UserNotActiveError(user_id=user_id)

    def create(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
    ) -> UserEntity:
        return self.repository.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
        )

    def save(self, user: UserEntity, update: bool = False) -> UserEntity:
        return self.repository.save(user=user, update=update)

    def try_get_by_id_with_loaded_seller(self, id: int) -> UserEntity:
        user = self.repository.get_by_id_with_loaded_seller(id=id)
        self._validate_user(user=user, user_id=id)
        return user

    def try_get_active_by_id(self, id: int) -> UserEntity:
        user = self.repository.get_by_id(id=id)
        self._validate_user(user=user, user_id=id)
        return user

    def set_password(self, user: UserEntity, password: str) -> None:
        return self.repository.set_password(user=user, password=password)

    def delete(self, id: int) -> None:
        self.repository.delete(id=id)
