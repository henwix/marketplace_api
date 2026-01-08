from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class CreateUserCommand:
    data: dict


@dataclass(frozen=True, eq=False)
class DeleteUserCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class UpdateUserCommand:
    user_id: int | None
    data: dict


@dataclass(frozen=True, eq=False)
class GetUserCommand:
    user_id: int | None


@dataclass(frozen=True, eq=False)
class SetPasswordUserCommand:
    user_id: int | None
    password: str
