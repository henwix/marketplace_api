from abc import ABC, abstractmethod

from django.db.models import Q

from src.apps.users.converters import user_from_entity, user_to_entity
from src.apps.users.entities import UserEntity
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
    def get_by_id_with_loaded_seller(self, id: int) -> User | None: ...

    @abstractmethod
    def get_by_id(self, id: int) -> User | None: ...

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
        dto = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
        )
        return user_to_entity(dto=dto)

    def save(self, user: User, update: bool) -> UserEntity:
        dto = user_from_entity(entity=user)
        dto.save(force_update=update)
        return user_to_entity(dto=dto)

    def set_password(self, user: User, password: str) -> None:
        dto = user_from_entity(entity=user)
        dto.set_password(password)
        dto.save()

    def get_by_id_with_loaded_seller(self, id: int) -> User | None:
        return User.objects.select_related('seller_profile').filter(pk=id).first()

    def get_by_id(self, id: int) -> User | None:
        return User.objects.filter(pk=id).first()

    def delete(self, id: int) -> None:
        User.objects.filter(pk=id).delete()

    def check_user_with_email_exists(self, email: str) -> bool:
        return self._check_user_exists_by_query(query=Q(email=email))

    def check_user_with_phone_exists(self, phone: str) -> bool:
        return self._check_user_exists_by_query(query=Q(phone=phone))
