from abc import ABC, abstractmethod

from django.db import IntegrityError
from django.db.models import Q

from src.apps.sellers.converters.sellers import seller_to_entity
from src.apps.users.converters import user_from_entity, user_to_entity
from src.apps.users.entities import UserEntity
from src.apps.users.exceptions.users import UserWithDataAlreadyExistsError
from src.apps.users.models import User


class BaseUserRepository(ABC):
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
    def save(self, user: User, update: bool) -> UserEntity: ...

    @abstractmethod
    def set_password(self, user: User, password: str) -> None: ...

    @abstractmethod
    def get_by_id_with_loaded_seller(self, id: int) -> UserEntity | None: ...

    @abstractmethod
    def get_by_id(self, id: int) -> UserEntity | None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...

    @abstractmethod
    def check_user_with_email_exists(self, email: str) -> bool: ...

    @abstractmethod
    def check_user_with_phone_exists(self, phone: str) -> bool: ...


class ORMUserRepository(BaseUserRepository):
    def _check_user_exists_by_query(self, query: Q) -> bool:
        return User.objects.filter(query).exists()

    def create(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
    ) -> UserEntity:
        try:
            dto = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password=password,
            )
            return user_to_entity(dto=dto)
        except IntegrityError:
            raise UserWithDataAlreadyExistsError

    def save(self, user: User, update: bool) -> UserEntity:
        try:
            dto = user_from_entity(entity=user)
            dto.save(force_update=update)
            return user_to_entity(dto=dto)
        except IntegrityError:
            raise UserWithDataAlreadyExistsError

    def set_password(self, user: User, password: str) -> None:
        dto = user_from_entity(entity=user)
        dto.set_password(password)
        dto.save()

    def get_by_id_with_loaded_seller(self, id: int) -> UserEntity | None:
        dto = User.objects.select_related('seller_profile').filter(pk=id).first()
        if dto is None:
            return None
        entity = user_to_entity(dto=dto)
        entity.seller_profile = seller_to_entity(dto=dto.seller_profile) if hasattr(dto, 'seller_profile') else None
        return entity

    def get_by_id(self, id: int) -> UserEntity | None:
        dto = User.objects.filter(pk=id).first()
        return user_to_entity(dto=dto) if dto else None

    def delete(self, id: int) -> None:
        User.objects.filter(pk=id).delete()

    def check_user_with_email_exists(self, email: str) -> bool:
        return self._check_user_exists_by_query(query=Q(email=email))

    def check_user_with_phone_exists(self, phone: str) -> bool:
        return self._check_user_exists_by_query(query=Q(phone=phone))
