from dataclasses import dataclass


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
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None


@dataclass(frozen=True, eq=False)
class DeleteUserCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class GetUserCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class SetPasswordUserCommand:
    user_id: int | None
    password: str
