from dataclasses import dataclass

from src.apps.common.types import UNSET, Unset


@dataclass(frozen=True, eq=False)
class CreateUserCommand:
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str


@dataclass(frozen=True, eq=False)
class UpdateUserCommand:
    user_id: int | None
    first_name: str | Unset = UNSET
    last_name: str | Unset = UNSET
    email: str | Unset = UNSET
    phone: str | Unset = UNSET


@dataclass(frozen=True, eq=False)
class DeleteUserCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class SetPasswordUserCommand:
    user_id: int | None
    password: str


@dataclass(frozen=True, eq=False)
class GetUserCommand:
    user_id: int | None
