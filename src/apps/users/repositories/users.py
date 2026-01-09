from abc import ABC, abstractmethod

from django.db.models import Q

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
    ) -> User: ...

    @abstractmethod
    def save(self, user: User, update: bool) -> User: ...

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
    ) -> User:
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
        )

    def save(self, user: User, update: bool) -> User:
        user.save(force_update=update)
        return user

    def set_password(self, user: User, password: str) -> None:
        user.set_password(password)
        user.save()

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
